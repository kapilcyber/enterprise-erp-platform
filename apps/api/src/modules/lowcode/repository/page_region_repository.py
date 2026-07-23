"""Low-Code LcPageRegion repository — Phase 3B."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.models import LcPageRegion
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow


class PageRegionRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcPageRegion | None:
        stmt = select(LcPageRegion).where(
            LcPageRegion.id == row_id,
            LcPageRegion.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcPageRegion, ctx)
        return self.db.scalar(stmt)

    def list_by_version(self, ctx: TenantContext, page_version_id: UUID):
        stmt = (
            select(LcPageRegion)
            .where(
                LcPageRegion.page_version_id == page_version_id,
                LcPageRegion.is_deleted.is_(False),
            )
            .order_by(LcPageRegion.display_order, LcPageRegion.region_code)
        )
        stmt = self.apply_lowcode_filter(stmt, LcPageRegion, ctx)
        return list(self.db.scalars(stmt).all())

    def create(self, ctx: TenantContext, **fields) -> LcPageRegion:
        row = LcPageRegion(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> LcPageRegion | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> LcPageRegion | None:
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
