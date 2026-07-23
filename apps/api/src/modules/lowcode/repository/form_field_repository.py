"""Low-Code LcFormField repository — Phase 2A."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.models import LcFormField
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow


class FormFieldRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcFormField | None:
        stmt = select(LcFormField).where(
            LcFormField.id == row_id,
            LcFormField.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormField, ctx)
        return self.db.scalar(stmt)

    def get_by_key(
        self, ctx: TenantContext, form_version_id: UUID, field_key: str
    ) -> LcFormField | None:
        stmt = select(LcFormField).where(
            LcFormField.form_version_id == form_version_id,
            LcFormField.field_key == field_key,
            LcFormField.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormField, ctx)
        return self.db.scalar(stmt)

    def list_by_version(self, ctx: TenantContext, form_version_id: UUID) -> list[LcFormField]:
        stmt = (
            select(LcFormField)
            .where(
                LcFormField.form_version_id == form_version_id,
                LcFormField.is_deleted.is_(False),
            )
            .order_by(LcFormField.display_order, LcFormField.field_label)
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormField, ctx)
        return list(self.db.scalars(stmt).all())

    def list_by_section(self, ctx: TenantContext, section_id: UUID) -> list[LcFormField]:
        stmt = (
            select(LcFormField)
            .where(
                LcFormField.section_id == section_id,
                LcFormField.is_deleted.is_(False),
            )
            .order_by(LcFormField.display_order, LcFormField.field_label)
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormField, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> LcFormField:
        row = LcFormField(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> LcFormField | None:
        row = self.get(ctx, row_id)
        if row is None:
            return None
        for k, v in fields.items():
            if v is not None:
                setattr(row, k, v)
        # Allow explicit nulling of section_id
        if "section_id" in fields and fields["section_id"] is None:
            row.section_id = None
        if "component_version_id" in fields and fields["component_version_id"] is None:
            row.component_version_id = None
        row.updated_at = utcnow()
        row.updated_by = ctx.user_id
        row.version = int(row.version or 1) + 1
        self.db.flush()
        return row

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> LcFormField | None:
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
