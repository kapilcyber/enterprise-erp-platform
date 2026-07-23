"""Low-Code LcLocalizationEntry repository — Phase 3A."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.models import LcLocalizationEntry
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow


class LocalizationEntryRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcLocalizationEntry | None:
        stmt = select(LcLocalizationEntry).where(
            LcLocalizationEntry.id == row_id,
            LcLocalizationEntry.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcLocalizationEntry, ctx)
        return self.db.scalar(stmt)

    def get_by_owner_key(
        self,
        ctx: TenantContext,
        *,
        owner_type: str,
        owner_ref_id: UUID,
        locale: str,
        translation_key: str,
    ) -> LcLocalizationEntry | None:
        stmt = select(LcLocalizationEntry).where(
            LcLocalizationEntry.owner_type == owner_type,
            LcLocalizationEntry.owner_ref_id == owner_ref_id,
            LcLocalizationEntry.locale == locale,
            LcLocalizationEntry.translation_key == translation_key,
            LcLocalizationEntry.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcLocalizationEntry, ctx)
        return self.db.scalar(stmt)

    def list_by_form_version(self, ctx: TenantContext, form_version_id: UUID):
        stmt = (
            select(LcLocalizationEntry)
            .where(
                LcLocalizationEntry.form_version_id == form_version_id,
                LcLocalizationEntry.is_deleted.is_(False),
            )
            .order_by(
                LcLocalizationEntry.locale,
                LcLocalizationEntry.translation_key,
            )
        )
        stmt = self.apply_lowcode_filter(stmt, LcLocalizationEntry, ctx)
        return list(self.db.scalars(stmt).all())

    def list_by_owner(self, ctx: TenantContext, owner_type: str, owner_ref_id: UUID):
        stmt = (
            select(LcLocalizationEntry)
            .where(
                LcLocalizationEntry.owner_type == owner_type,
                LcLocalizationEntry.owner_ref_id == owner_ref_id,
                LcLocalizationEntry.is_deleted.is_(False),
            )
            .order_by(
                LcLocalizationEntry.locale,
                LcLocalizationEntry.translation_key,
            )
        )
        stmt = self.apply_lowcode_filter(stmt, LcLocalizationEntry, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> LcLocalizationEntry:
        row = LcLocalizationEntry(
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
    ) -> LcLocalizationEntry | None:
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

    def soft_delete(
        self, ctx: TenantContext, row_id: UUID
    ) -> LcLocalizationEntry | None:
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
