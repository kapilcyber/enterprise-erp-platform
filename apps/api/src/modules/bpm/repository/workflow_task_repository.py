"""Workflow task repository — Phase 4."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.bpm.models import BpmWorkflowTask
from modules.bpm.repository.base import BpmScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext


class WorkflowTaskRepository(BpmScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowTask | None:
        stmt = select(BpmWorkflowTask).where(
            BpmWorkflowTask.id == row_id,
            BpmWorkflowTask.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowTask, ctx)
        return self.db.scalar(stmt)

    def list_by_instance(self, ctx: TenantContext, instance_id: UUID) -> list[BpmWorkflowTask]:
        stmt = (
            select(BpmWorkflowTask)
            .where(
                BpmWorkflowTask.instance_id == instance_id,
                BpmWorkflowTask.is_deleted.is_(False),
            )
            .order_by(BpmWorkflowTask.sequence_order, BpmWorkflowTask.task_name)
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowTask, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> BpmWorkflowTask:
        row = BpmWorkflowTask(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> BpmWorkflowTask | None:
        row = self.get(ctx, row_id)
        if row is None:
            return None
        for k, v in fields.items():
            if v is not None:
                setattr(row, k, v)
        row.updated_at = utcnow()
        row.updated_by = ctx.user_id
        row.version = int(row.version or 1) + 1
        self.db.flush()
        return row

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowTask | None:
        row = self.get(ctx, row_id)
        if row is None:
            return None
        row.is_deleted = True
        row.deleted_at = utcnow()
        row.deleted_by = ctx.user_id
        row.updated_at = utcnow()
        row.updated_by = ctx.user_id
        row.version = int(row.version or 1) + 1
        self.db.flush()
        return row
