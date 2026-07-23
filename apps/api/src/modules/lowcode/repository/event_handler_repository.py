"""Low-Code LcEventHandler repository — Phase 3A."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.models import LcEventHandler
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow


class EventHandlerRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcEventHandler | None:
        stmt = select(LcEventHandler).where(
            LcEventHandler.id == row_id,
            LcEventHandler.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcEventHandler, ctx)
        return self.db.scalar(stmt)

    def list_by_form_version(self, ctx: TenantContext, form_version_id: UUID):
        stmt = (
            select(LcEventHandler)
            .where(
                LcEventHandler.form_version_id == form_version_id,
                LcEventHandler.is_deleted.is_(False),
            )
            .order_by(LcEventHandler.execution_order, LcEventHandler.handler_code)
        )
        stmt = self.apply_lowcode_filter(stmt, LcEventHandler, ctx)
        return list(self.db.scalars(stmt).all())

    def list_by_field(self, ctx: TenantContext, field_id: UUID):
        stmt = (
            select(LcEventHandler)
            .where(
                LcEventHandler.field_id == field_id,
                LcEventHandler.is_deleted.is_(False),
            )
            .order_by(LcEventHandler.execution_order, LcEventHandler.handler_code)
        )
        stmt = self.apply_lowcode_filter(stmt, LcEventHandler, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> LcEventHandler:
        row = LcEventHandler(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> LcEventHandler | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> LcEventHandler | None:
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
