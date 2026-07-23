"""Low-Code LcComponent repository — Phase 2B."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.domain.value_objects import PageResult
from modules.lowcode.models import LcComponent
from modules.lowcode.repository.base import LowcodeScopedRepository, utcnow

_SORT = {
    "component_code",
    "component_name",
    "component_kind",
    "status",
    "created_at",
    "updated_at",
}


class ComponentRepository(LowcodeScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> LcComponent | None:
        stmt = select(LcComponent).where(
            LcComponent.id == row_id,
            LcComponent.is_deleted.is_(False),
        )
        stmt = self.apply_lowcode_filter(stmt, LcComponent, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> LcComponent | None:
        stmt = select(LcComponent).where(LcComponent.id == row_id)
        stmt = self.apply_lowcode_filter(stmt, LcComponent, ctx)
        return self.db.scalar(stmt)

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
        *,
        status: str | None = None,
        component_kind: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "component_name",
        sort_dir: str = "asc",
        include_archived: bool = False,
    ) -> PageResult:
        stmt = select(LcComponent).where(LcComponent.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(LcComponent.is_deleted.is_(False))
        if status:
            stmt = stmt.where(LcComponent.status == status)
        if component_kind:
            stmt = stmt.where(LcComponent.component_kind == component_kind)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                LcComponent.component_name.ilike(like)
                | LcComponent.component_code.ilike(like)
            )
        stmt = self.apply_lowcode_filter(stmt, LcComponent, ctx)
        return self.paginate_sorted(
            stmt,
            LcComponent,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> LcComponent:
        row = LcComponent(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> LcComponent | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> LcComponent | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> LcComponent | None:
        row = self.get_including_archived(ctx, row_id)
        if row is None or not row.is_deleted:
            return None
        row.is_deleted = False
        row.deleted_at = None
        row.deleted_by = None
        row.updated_at = utcnow()
        row.updated_by = ctx.user_id
        row.version = int(row.version or 1) + 1
        self.db.flush()
        return row
