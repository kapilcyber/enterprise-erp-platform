"""Low-Code LcFormSection repository — Phase 2A."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.models import LcFormSection
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow


class FormSectionRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcFormSection | None:
        stmt = select(LcFormSection).where(
            LcFormSection.id == row_id,
            LcFormSection.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormSection, ctx)
        return self.db.scalar(stmt)

    def list_by_version(self, ctx: TenantContext, form_version_id: UUID) -> list[LcFormSection]:
        stmt = (
            select(LcFormSection)
            .where(
                LcFormSection.form_version_id == form_version_id,
                LcFormSection.is_deleted.is_(False),
            )
            .order_by(LcFormSection.display_order, LcFormSection.section_name)
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormSection, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> LcFormSection:
        row = LcFormSection(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> LcFormSection | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> LcFormSection | None:
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
