"""Low-Code LcFormVersion repository — Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.domain.enums import VersionStatus
from modules.lowcode.models import LcFormVersion
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow


class FormVersionRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcFormVersion | None:
        stmt = select(LcFormVersion).where(
            LcFormVersion.id == row_id,
            LcFormVersion.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormVersion, ctx)
        return self.db.scalar(stmt)

    def list_by_definition(self, ctx: TenantContext, definition_id: UUID):
        stmt = select(LcFormVersion).where(
            LcFormVersion.definition_id == definition_id,
            LcFormVersion.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormVersion, ctx)
        stmt = stmt.order_by(LcFormVersion.version_number.desc())
        return list(self.db.scalars(stmt).all())

    def get_published(self, ctx: TenantContext, definition_id: UUID) -> LcFormVersion | None:
        stmt = select(LcFormVersion).where(
            LcFormVersion.definition_id == definition_id,
            LcFormVersion.status == VersionStatus.PUBLISHED.value,
            LcFormVersion.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormVersion, ctx)
        return self.db.scalar(stmt)

    def count_published(self, ctx: TenantContext, definition_id: UUID) -> int:
        stmt = select(func.count()).select_from(LcFormVersion).where(
            LcFormVersion.definition_id == definition_id,
            LcFormVersion.status == VersionStatus.PUBLISHED.value,
            LcFormVersion.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcFormVersion, ctx)
        return int(self.db.scalar(stmt) or 0)

    def next_version_number(self, ctx: TenantContext, definition_id: UUID) -> int:
        rows = self.list_by_definition(ctx, definition_id)
        if not rows:
            return 1
        return max(r.version_number for r in rows) + 1

    def create(self, ctx: TenantContext, **fields) -> LcFormVersion:
        row = LcFormVersion(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> LcFormVersion | None:
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
