"""Low-Code LcExpressionBinding repository — Phase 2C."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.models import LcExpressionBinding
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow


class ExpressionBindingRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcExpressionBinding | None:
        stmt = select(LcExpressionBinding).where(
            LcExpressionBinding.id == row_id,
            LcExpressionBinding.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcExpressionBinding, ctx)
        return self.db.scalar(stmt)

    def list_by_expression(self, ctx: TenantContext, expression_id: UUID):
        stmt = (
            select(LcExpressionBinding)
            .where(
                LcExpressionBinding.expression_id == expression_id,
                LcExpressionBinding.is_deleted.is_(False),
            )
            .order_by(LcExpressionBinding.sort_order, LcExpressionBinding.binding_code)
        )
        stmt = self.apply_lowcode_filter(stmt, LcExpressionBinding, ctx)
        return list(self.db.scalars(stmt).all())

    def list_by_form_version(self, ctx: TenantContext, form_version_id: UUID):
        stmt = (
            select(LcExpressionBinding)
            .where(
                LcExpressionBinding.form_version_id == form_version_id,
                LcExpressionBinding.is_deleted.is_(False),
            )
            .order_by(LcExpressionBinding.sort_order, LcExpressionBinding.binding_code)
        )
        stmt = self.apply_lowcode_filter(stmt, LcExpressionBinding, ctx)
        return list(self.db.scalars(stmt).all())

    def list_by_field(self, ctx: TenantContext, field_id: UUID):
        stmt = (
            select(LcExpressionBinding)
            .where(
                LcExpressionBinding.field_id == field_id,
                LcExpressionBinding.is_deleted.is_(False),
            )
            .order_by(LcExpressionBinding.sort_order, LcExpressionBinding.binding_code)
        )
        stmt = self.apply_lowcode_filter(stmt, LcExpressionBinding, ctx)
        return list(self.db.scalars(stmt).all())

    def list_by_section(self, ctx: TenantContext, section_id: UUID):
        stmt = (
            select(LcExpressionBinding)
            .where(
                LcExpressionBinding.section_id == section_id,
                LcExpressionBinding.is_deleted.is_(False),
            )
            .order_by(LcExpressionBinding.sort_order, LcExpressionBinding.binding_code)
        )
        stmt = self.apply_lowcode_filter(stmt, LcExpressionBinding, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> LcExpressionBinding:
        row = LcExpressionBinding(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> LcExpressionBinding | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> LcExpressionBinding | None:
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
