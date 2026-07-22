"""TaskDelegationService — Phase 4."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType, DelegationStatus, HistoryEventType
from modules.bpm.domain.exceptions import InvalidTaskDelegationState
from modules.bpm.models import BpmTaskDelegation
from modules.bpm.repository.task_delegation_repository import TaskDelegationRepository
from modules.bpm.repository.workflow_task_repository import WorkflowTaskRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.bpm.service.engines import TaskDelegationEngine
from modules.bpm.service.workflow_history_service import WorkflowHistoryService
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class TaskDelegationService:
    def __init__(self, db: Session) -> None:
        self._repo = TaskDelegationRepository(db)
        self._tasks = WorkflowTaskRepository(db)
        self._scope = BpmScopeValidator(db)
        self._numbers = BpmNumberService(db)
        self._engine = TaskDelegationEngine()
        self._history = WorkflowHistoryService(db)
        self._audit = AuditService(db)

    def list_by_task(self, ctx: TenantContext, task_id: UUID):
        if self._tasks.get(ctx, task_id) is None:
            raise NotFoundException("Workflow task not found")
        return self._repo.list_by_task(ctx, task_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmTaskDelegation:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Task delegation not found")
        return row

    def create(
        self,
        ctx: TenantContext,
        task_id: UUID,
        *,
        original_assignee_id: UUID,
        delegate_assignee_id: UUID,
        effective_from: datetime | None = None,
        effective_to: datetime | None = None,
        reason: str | None = None,
        company_id: UUID | None = None,
    ):
        task = self._tasks.get(ctx, task_id)
        if task is None:
            raise NotFoundException("Workflow task not found")
        if original_assignee_id == delegate_assignee_id:
            raise InvalidTaskDelegationState(
                "original_assignee_id and delegate_assignee_id must differ"
            )
        eff_from = effective_from or datetime.now(timezone.utc)
        self._engine.assert_period(eff_from, effective_to)
        cid = self._scope.resolve_company_id(ctx, company_id or task.company_id)
        code = self._numbers.generate(
            BpmEntityType.TASK_DELEGATION, cid, BpmTaskDelegation, "delegation_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            task_id=task_id,
            delegation_code=code,
            status=DelegationStatus.PENDING.value,
            original_assignee_id=original_assignee_id,
            delegate_assignee_id=delegate_assignee_id,
            effective_from=eff_from,
            effective_to=effective_to,
            reason=reason,
        )
        self._history.append(
            ctx,
            task.instance_id,
            event_type=HistoryEventType.DELEGATION.value,
            company_id=cid,
            task_id=task_id,
            delegation_id=row.id,
            from_status=None,
            to_status=row.status,
            message=reason or "delegated",
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="bpm_task_delegation",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def accept(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        task = self._tasks.get(ctx, row.task_id)
        if task is None:
            raise NotFoundException("Workflow task not found")
        prev = row.status
        self._engine.accept(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, accepted_at=row.accepted_at
        )
        if updated is None:
            raise NotFoundException("Task delegation not found")
        # Move current assignee to delegate
        self._tasks.update(ctx, task.id, assignee_id=row.delegate_assignee_id)
        self._history.append(
            ctx,
            task.instance_id,
            event_type=HistoryEventType.DELEGATION.value,
            company_id=task.company_id,
            task_id=task.id,
            delegation_id=row_id,
            from_status=prev,
            to_status=updated.status,
            message="delegation accepted",
        )
        return updated

    def reject(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        task = self._tasks.get(ctx, row.task_id)
        if task is None:
            raise NotFoundException("Workflow task not found")
        prev = row.status
        self._engine.reject(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, rejected_at=row.rejected_at
        )
        if updated is None:
            raise NotFoundException("Task delegation not found")
        self._history.append(
            ctx,
            task.instance_id,
            event_type=HistoryEventType.DELEGATION.value,
            company_id=task.company_id,
            task_id=task.id,
            delegation_id=row_id,
            from_status=prev,
            to_status=updated.status,
            message="delegation rejected",
        )
        return updated

    def expire(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        task = self._tasks.get(ctx, row.task_id)
        if task is None:
            raise NotFoundException("Workflow task not found")
        prev = row.status
        self._engine.expire(row)
        updated = self._repo.update(
            ctx, row_id, status=row.status, expired_at=row.expired_at
        )
        if updated is None:
            raise NotFoundException("Task delegation not found")
        self._history.append(
            ctx,
            task.instance_id,
            event_type=HistoryEventType.DELEGATION.value,
            company_id=task.company_id,
            task_id=task.id,
            delegation_id=row_id,
            from_status=prev,
            to_status=updated.status,
            message="delegation expired",
        )
        return updated

    def soft_delete(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        if row.status == DelegationStatus.ACCEPTED.value:
            raise InvalidTaskDelegationState("Cannot delete an accepted delegation — expire it")
        deleted = self._repo.soft_delete(ctx, row_id)
        if deleted is None:
            raise NotFoundException("Task delegation not found")
        return deleted
