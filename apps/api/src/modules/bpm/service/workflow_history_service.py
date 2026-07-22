"""WorkflowHistoryService — Phase 4 append-only."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.enums import BpmEntityType
from modules.bpm.domain.exceptions import HistoryAppendOnlyViolation
from modules.bpm.models import BpmWorkflowHistory
from modules.bpm.repository.base import utcnow
from modules.bpm.repository.workflow_history_repository import WorkflowHistoryRepository
from modules.bpm.repository.workflow_instance_repository import WorkflowInstanceRepository
from modules.bpm.service.bpm_number_service import BpmNumberService
from modules.bpm.service.engines import WorkflowHistoryEngine
from modules.foundation.domain.value_objects import TenantContext


class WorkflowHistoryService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowHistoryRepository(db)
        self._instances = WorkflowInstanceRepository(db)
        self._numbers = BpmNumberService(db)
        self._engine = WorkflowHistoryEngine()

    def list_by_instance(self, ctx: TenantContext, instance_id: UUID):
        if self._instances.get(ctx, instance_id) is None:
            raise NotFoundException("Workflow instance not found")
        return self._repo.list_by_instance(ctx, instance_id)

    def list_by_task(self, ctx: TenantContext, task_id: UUID):
        return self._repo.list_by_task(ctx, task_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowHistory:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Workflow history event not found")
        return row

    def append(
        self,
        ctx: TenantContext,
        instance_id: UUID,
        *,
        event_type: str,
        company_id: UUID,
        task_id: UUID | None = None,
        delegation_id: UUID | None = None,
        from_status: str | None = None,
        to_status: str | None = None,
        message: str | None = None,
        payload_json: str | None = None,
        actor_id: UUID | None = None,
    ) -> BpmWorkflowHistory:
        self._engine.assert_event_type(event_type)
        instance = self._instances.get(ctx, instance_id)
        if instance is None:
            raise NotFoundException("Workflow instance not found")
        code = self._numbers.generate(
            BpmEntityType.WORKFLOW_HISTORY, company_id, BpmWorkflowHistory, "event_code"
        )
        return self._repo.append(
            ctx,
            company_id=company_id,
            instance_id=instance_id,
            task_id=task_id,
            delegation_id=delegation_id,
            event_code=code,
            event_type=event_type,
            from_status=from_status,
            to_status=to_status,
            message=message,
            payload_json=payload_json,
            actor_id=actor_id or ctx.user_id,
            occurred_at=utcnow(),
        )

    def update(self, *_args, **_kwargs):
        raise HistoryAppendOnlyViolation()

    def soft_delete(self, *_args, **_kwargs):
        raise HistoryAppendOnlyViolation()
