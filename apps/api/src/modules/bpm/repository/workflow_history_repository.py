"""Workflow history repository — Phase 4 (append-only)."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.bpm.models import BpmWorkflowHistory
from modules.bpm.repository.base import BpmScopedRepository
from modules.foundation.domain.value_objects import TenantContext


class WorkflowHistoryRepository(BpmScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowHistory | None:
        stmt = select(BpmWorkflowHistory).where(
            BpmWorkflowHistory.id == row_id,
            BpmWorkflowHistory.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowHistory, ctx)
        return self.db.scalar(stmt)

    def list_by_instance(
        self, ctx: TenantContext, instance_id: UUID
    ) -> list[BpmWorkflowHistory]:
        stmt = (
            select(BpmWorkflowHistory)
            .where(
                BpmWorkflowHistory.instance_id == instance_id,
                BpmWorkflowHistory.is_deleted.is_(False),
            )
            .order_by(BpmWorkflowHistory.occurred_at.asc())
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowHistory, ctx)
        return list(self.db.scalars(stmt).all())

    def list_by_task(self, ctx: TenantContext, task_id: UUID) -> list[BpmWorkflowHistory]:
        stmt = (
            select(BpmWorkflowHistory)
            .where(
                BpmWorkflowHistory.task_id == task_id,
                BpmWorkflowHistory.is_deleted.is_(False),
            )
            .order_by(BpmWorkflowHistory.occurred_at.asc())
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowHistory, ctx)
        return list(self.db.scalars(stmt).all())

    def append(self, ctx: TenantContext, **fields) -> BpmWorkflowHistory:
        """Append-only create — no update / soft-delete API on this repository."""
        row = BpmWorkflowHistory(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row
