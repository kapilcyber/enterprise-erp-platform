"""WorkflowInstanceService — Phase 4 (Published version only)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, HistoryEventType, InstanceStatus
from modules.bpm.domain.exceptions import InvalidWorkflowInstanceState
from modules.bpm.models import BpmWorkflowInstance
from modules.bpm.repository.workflow_instance_repository import WorkflowInstanceRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import WorkflowInstanceEngine, WorkflowVersionEngine
from modules.bpm.service.graph_driven_task_generation_service import (
    GraphDrivenTaskGenerationService,
)
from modules.bpm.service.workflow_history_service import WorkflowHistoryService
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class WorkflowInstanceService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowInstanceRepository(db)
        self._versions = WorkflowVersionRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = WorkflowInstanceEngine()
        self._version_engine = WorkflowVersionEngine()
        self._history = WorkflowHistoryService(db)
        self._audit = AuditService(db)
        self._graph_tasks = GraphDrivenTaskGenerationService(db)

    def _require_published_version(self, ctx: TenantContext, version_id: UUID):
        version = self._versions.get(ctx, version_id)
        if version is None:
            raise NotFoundException("Workflow version not found")
        self._version_engine.assert_executable(version)
        return version

    def _record(
        self,
        ctx: TenantContext,
        row: BpmWorkflowInstance,
        *,
        from_status: str | None,
        to_status: str,
        message: str | None = None,
    ):
        self._history.append(
            ctx,
            row.id,
            event_type=HistoryEventType.STATE_TRANSITION.value,
            company_id=row.company_id,
            from_status=from_status,
            to_status=to_status,
            message=message,
        )

    def list_by_version(self, ctx: TenantContext, version_id: UUID):
        if self._versions.get(ctx, version_id) is None:
            raise NotFoundException("Workflow version not found")
        return self._repo.list_by_version(ctx, version_id)

    def list_by_business_entity(self, ctx: TenantContext, module_code: str, entity_id: UUID):
        return self._repo.list_by_business_entity(ctx, module_code, entity_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowInstance:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow instance not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        version_id: UUID,
        *,
        module_code: str,
        entity_id: UUID,
        company_id: UUID | None = None,
        entity_type: str | None = None,
        description: str | None = None,
        context_json: str | None = None,
        auto_start: bool = False,
    ):
        version = self._require_published_version(ctx, version_id)
        self._engine.assert_business_ref(module_code, entity_id)
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = self._numbers.generate(
            BpmEntityType.WORKFLOW_INSTANCE, cid, BpmWorkflowInstance, "instance_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            version_id=version_id,
            definition_id=version.definition_id,
            instance_code=code,
            status=InstanceStatus.PENDING.value,
            module_code=module_code,
            entity_id=entity_id,
            entity_type=entity_type,
            description=description,
            context_json=context_json,
        )
        self._record(
            ctx, row, from_status=None, to_status=InstanceStatus.PENDING.value, message="created"
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_instance",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        if auto_start:
            return self.start(ctx, row.id)
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        if row.status in {
            InstanceStatus.COMPLETED.value,
            InstanceStatus.CANCELLED.value,
            InstanceStatus.FAILED.value,
        }:
            raise InvalidWorkflowInstanceState("Terminal instances cannot be updated")
        allowed = {"description", "context_json"}
        payload = {k: v for k, v in fields.items() if k in allowed and v is not None}
        updated = self._repo.update(ctx, row_id, **payload)
        if updated is None:
            raise NotFoundException("Workflow instance not found")
        return updated

    def start(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_published_version(ctx, row.version_id)
        prev = row.status
        self._engine.start(row)
        row.started_by = ctx.user_id
        updated = self._repo.update(
            ctx, row_id, status=row.status, started_at=row.started_at, started_by=row.started_by
        )
        if updated is None:
            raise NotFoundException("Workflow instance not found")
        self._record(ctx, updated, from_status=prev, to_status=updated.status, message="started")
        # Phase 5 polish: seed tasks from published designer graph (reuse WorkflowTaskService).
        self._graph_tasks.generate_initial_tasks(ctx, updated)
        return updated

    def cancel(self, ctx: TenantContext, row_id: UUID, *, reason: str | None = None):
        row = self.get(ctx, row_id)
        prev = row.status
        self._engine.cancel(row, reason=reason)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            cancel_reason=row.cancel_reason,
            completed_at=row.completed_at,
        )
        if updated is None:
            raise NotFoundException("Workflow instance not found")
        self._record(ctx, updated, from_status=prev, to_status=updated.status, message=reason)
        return updated

    def suspend(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        prev = row.status
        self._engine.suspend(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, suspended_at=row.suspended_at
        )
        if updated is None:
            raise NotFoundException("Workflow instance not found")
        self._record(ctx, updated, from_status=prev, to_status=updated.status, message="suspended")
        return updated

    def resume(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        prev = row.status
        self._engine.resume(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("Workflow instance not found")
        updated.suspended_at = None
        self._record(ctx, updated, from_status=prev, to_status=updated.status, message="resumed")
        return updated

    def complete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        prev = row.status
        self._engine.complete(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, completed_at=row.completed_at
        )
        if updated is None:
            raise NotFoundException("Workflow instance not found")
        self._record(ctx, updated, from_status=prev, to_status=updated.status, message="completed")
        return updated

    def fail(self, ctx: TenantContext, row_id: UUID, *, reason: str | None = None):
        row = self.get(ctx, row_id)
        prev = row.status
        self._engine.fail(row, reason=reason)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            failure_reason=row.failure_reason,
            completed_at=row.completed_at,
        )
        if updated is None:
            raise NotFoundException("Workflow instance not found")
        self._record(ctx, updated, from_status=prev, to_status=updated.status, message=reason)
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        if row.status == InstanceStatus.RUNNING.value:
            raise InvalidWorkflowInstanceState("Cannot delete a running instance — cancel first")
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Workflow instance not found")
        return deleted
