"""Low-Code LcComponentVersion repository — Phase 2B."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.domain.enums import VersionStatus
from modules.lowcode.models import LcComponentVersion
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow


class ComponentVersionRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcComponentVersion | None:
        stmt = select(LcComponentVersion).where(
            LcComponentVersion.id == row_id,
            LcComponentVersion.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcComponentVersion, ctx)
        return self.db.scalar(stmt)

    def list_by_component(self, ctx: TenantContext, component_id: UUID):
        stmt = select(LcComponentVersion).where(
            LcComponentVersion.component_id == component_id,
            LcComponentVersion.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcComponentVersion, ctx)
        stmt = stmt.order_by(LcComponentVersion.version_number.desc())
        return list(self.db.scalars(stmt).all())

    def get_published(
        self, ctx: TenantContext, component_id: UUID
    ) -> LcComponentVersion | None:
        stmt = select(LcComponentVersion).where(
            LcComponentVersion.component_id == component_id,
            LcComponentVersion.status == VersionStatus.PUBLISHED.value,
            LcComponentVersion.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcComponentVersion, ctx)
        return self.db.scalar(stmt)

    def next_version_number(self, ctx: TenantContext, component_id: UUID) -> int:
        rows = self.list_by_component(ctx, component_id)
        if not rows:
            return 1
        return max(r.version_number for r in rows) + 1

    def create(self, ctx: TenantContext, **fields) -> LcComponentVersion:
        row = LcComponentVersion(
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
    ) -> LcComponentVersion | None:
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
