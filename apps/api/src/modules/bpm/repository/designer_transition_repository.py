"""BPM BpmDesignerTransition repository — Phase 2A."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.bpm.models import BpmDesignerTransition
from modules.bpm.repository.base import BpmScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext


class DesignerTransitionRepository(BpmScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmDesignerTransition | None:
        stmt = select(BpmDesignerTransition).where(
            BpmDesignerTransition.id == row_id,
            BpmDesignerTransition.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmDesignerTransition, ctx)
        return self.db.scalar(stmt)

    def list_by_version(
        self, ctx: TenantContext, version_id: UUID
    ) -> list[BpmDesignerTransition]:
        stmt = (
            select(BpmDesignerTransition)
            .where(
                BpmDesignerTransition.version_id == version_id,
                BpmDesignerTransition.is_deleted.is_(False),
            )
            .order_by(BpmDesignerTransition.priority, BpmDesignerTransition.transition_name)
        )
        stmt = self.apply_bpm_filter(stmt, BpmDesignerTransition, ctx)
        return list(self.db.scalars(stmt).all())

    def find_edge(
        self,
        ctx: TenantContext,
        version_id: UUID,
        from_node_id: UUID,
        to_node_id: UUID,
    ) -> BpmDesignerTransition | None:
        stmt = select(BpmDesignerTransition).where(
            BpmDesignerTransition.version_id == version_id,
            BpmDesignerTransition.from_node_id == from_node_id,
            BpmDesignerTransition.to_node_id == to_node_id,
            BpmDesignerTransition.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmDesignerTransition, ctx)
        return self.db.scalar(stmt)

    def list_involving_node(
        self, ctx: TenantContext, version_id: UUID, node_id: UUID
    ) -> list[BpmDesignerTransition]:
        stmt = select(BpmDesignerTransition).where(
            BpmDesignerTransition.version_id == version_id,
            BpmDesignerTransition.is_deleted.is_(False),
            (BpmDesignerTransition.from_node_id == node_id)
            | (BpmDesignerTransition.to_node_id == node_id),
        )
        stmt = self.apply_bpm_filter(stmt, BpmDesignerTransition, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> BpmDesignerTransition:
        row = BpmDesignerTransition(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(
        self, ctx: TenantContext, row_id: UUID, **fields
    ) -> BpmDesignerTransition | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> BpmDesignerTransition | None:
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
