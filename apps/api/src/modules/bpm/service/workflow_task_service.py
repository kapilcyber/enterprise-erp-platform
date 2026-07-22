"""WorkflowTaskService — Phase 4."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import (
    BpmEntityType,
    HistoryEventType,
    InstanceStatus,
    TaskExecutionMode,
    TaskStatus,
)
from modules.bpm.domain.exceptions import InvalidWorkflowTaskState
from modules.bpm.models import BpmWorkflowTask
from modules.bpm.repository.workflow_instance_repository import WorkflowInstanceRepository
from modules.bpm.repository.workflow_task_repository import WorkflowTaskRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import WorkflowTaskEngine
from modules.bpm.service.workflow_history_service import WorkflowHistoryService
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class WorkflowTaskService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowTaskRepository(db)
        self._instances = WorkflowInstanceRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = WorkflowTaskEngine()
        self._history = WorkflowHistoryService(db)
        self._audit = AuditService(db)

    def _require_active_instance(self, ctx: TenantContext, instance_id: UUID):
        instance = self._instances.get(ctx, instance_id)
        if instance is None:
            raise NotFoundException("Workflow instance not found")
        if instance.status not in {
            InstanceStatus.RUNNING.value,
            InstanceStatus.SUSPENDED.value,
            InstanceStatus.PENDING.value,
        }:
            raise InvalidWorkflowTaskState(
                "Tasks can only be managed on active (non-terminal) instances"
            )
        return instance

    def list_by_instance(self, ctx: TenantContext, instance_id: UUID):
        if self._instances.get(ctx, instance_id) is None:
            raise NotFoundException("Workflow instance not found")
        return self._repo.list_by_instance(ctx, instance_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowTask:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow task not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        instance_id: UUID,
        *,
        task_name: str,
        company_id: UUID | None = None,
        **fields,
    ):
        instance = self._require_active_instance(ctx, instance_id)
        mode = fields.get("execution_mode") or TaskExecutionMode.SEQUENTIAL.value
        fields["execution_mode"] = mode
        self._engine.assert_execution_mode(mode)
        cid = self._scope.resolve_company_id(ctx, company_id or instance.company_id)
        code = fields.pop("task_code", None) or self._numbers.generate(
            BpmEntityType.WORKFLOW_TASK, cid, BpmWorkflowTask, "task_code"
        )
        if "status" not in fields or fields["status"] is None:
            fields["status"] = TaskStatus.OPEN.value
        fields.setdefault("priority", 0)
        fields.setdefault("sequence_order", 0)
        row = self._repo.create(
            ctx,
            company_id=cid,
            instance_id=instance_id,
            task_code=code,
            task_name=task_name,
            **fields,
        )
        self._history.append(
            ctx,
            instance_id,
            event_type=HistoryEventType.STATE_TRANSITION.value,
            company_id=cid,
            task_id=row.id,
            from_status=None,
            to_status=row.status,
            message="task created",
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_workflow_task",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._require_active_instance(ctx, row.instance_id)
        if "execution_mode" in fields and fields["execution_mode"] is not None:
            self._engine.assert_execution_mode(fields["execution_mode"])
        allowed = {
            "task_name",
            "description",
            "priority",
            "execution_mode",
            "parallel_group_key",
            "sequence_order",
            "due_at",
            "metadata_json",
            "node_id",
        }
        payload = {k: v for k, v in fields.items() if k in allowed and v is not None}
        updated = self._repo.update(ctx, row_id, **payload)
        if updated is None:
            raise NotFoundException("Workflow task not found")
        return updated

    def assign(self, ctx: TenantContext, row_id: UUID, assignee_id: UUID):
        row = self.get(ctx, row_id)
        instance = self._require_active_instance(ctx, row.instance_id)
        prev = row.status
        self._engine.assign(row, assignee_id)
        updated = self._repo.update(
            ctx, row_id, status=row.status, assignee_id=row.assignee_id, claimed_by=row.claimed_by
        )
        if updated is None:
            raise NotFoundException("Workflow task not found")
        self._history.append(
            ctx,
            instance.id,
            event_type=HistoryEventType.ASSIGNMENT.value,
            company_id=instance.company_id,
            task_id=row_id,
            from_status=prev,
            to_status=updated.status,
            message=f"assigned to {assignee_id}",
        )
        return updated

    def claim(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        instance = self._require_active_instance(ctx, row.instance_id)
        prev = row.status
        self._engine.claim(row, ctx.user_id)
        updated = self._repo.update(
            ctx, row_id, status=row.status, assignee_id=row.assignee_id, claimed_by=row.claimed_by
        )
        if updated is None:
            raise NotFoundException("Workflow task not found")
        self._history.append(
            ctx,
            instance.id,
            event_type=HistoryEventType.ASSIGNMENT.value,
            company_id=instance.company_id,
            task_id=row_id,
            from_status=prev,
            to_status=updated.status,
            message="claimed",
        )
        return updated

    def release(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        instance = self._require_active_instance(ctx, row.instance_id)
        prev = row.status
        self._engine.release(row)
        updated = self._repo.update(ctx, row_id, status=row.status, claimed_by=row.claimed_by)
        if updated is None:
            raise NotFoundException("Workflow task not found")
        self._history.append(
            ctx,
            instance.id,
            event_type=HistoryEventType.ASSIGNMENT.value,
            company_id=instance.company_id,
            task_id=row_id,
            from_status=prev,
            to_status=updated.status,
            message="released",
        )
        return updated

    def complete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        instance = self._require_active_instance(ctx, row.instance_id)
        prev = row.status
        self._engine.complete(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, completed_at=row.completed_at
        )
        if updated is None:
            raise NotFoundException("Workflow task not found")
        self._history.append(
            ctx,
            instance.id,
            event_type=HistoryEventType.APPROVAL.value,
            company_id=instance.company_id,
            task_id=row_id,
            from_status=prev,
            to_status=updated.status,
            message="completed",
        )
        return updated

    def reject(self, ctx: TenantContext, row_id: UUID, *, reason: str | None = None):
        row = self.get(ctx, row_id)
        instance = self._require_active_instance(ctx, row.instance_id)
        prev = row.status
        self._engine.reject(row, reason=reason)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            rejection_reason=row.rejection_reason,
            completed_at=row.completed_at,
        )
        if updated is None:
            raise NotFoundException("Workflow task not found")
        self._history.append(
            ctx,
            instance.id,
            event_type=HistoryEventType.REJECTION.value,
            company_id=instance.company_id,
            task_id=row_id,
            from_status=prev,
            to_status=updated.status,
            message=reason,
        )
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._require_active_instance(ctx, row.instance_id)
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Workflow task not found")
        return deleted
