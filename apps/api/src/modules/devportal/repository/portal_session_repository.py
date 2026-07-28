"""DpPortalSession repository — Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.devportal.domain.value_objects import PageResult
from modules.devportal.models.portal_session import DpPortalSession
from modules.devportal.repository.base import DevportalScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext

_SORT = {"session_ref", "status", "created_at", "updated_at", "sort_order"}


class PortalSessionRepository(DevportalScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> DpPortalSession | None:
        stmt = select(DpPortalSession).where(
            DpPortalSession.id == row_id,
            DpPortalSession.is_deleted.is_(False),
        )
        stmt = self.apply_devportal_filter(stmt, DpPortalSession, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> DpPortalSession | None:
        stmt = select(DpPortalSession).where(DpPortalSession.id == row_id)
        stmt = self.apply_devportal_filter(stmt, DpPortalSession, ctx)
        return self.db.scalar(stmt)

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "created_at",
        sort_dir: str = "asc",
        include_archived: bool = False,
    ) -> PageResult:
        stmt = select(DpPortalSession).where(DpPortalSession.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(DpPortalSession.is_deleted.is_(False))
        if status:
            stmt = stmt.where(DpPortalSession.status == status)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(DpPortalSession.session_ref.ilike(like))
        stmt = self.apply_devportal_filter(stmt, DpPortalSession, ctx)
        return self.paginate_sorted(
            stmt,
            DpPortalSession,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> DpPortalSession:
        row = DpPortalSession(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> DpPortalSession | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> DpPortalSession | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> DpPortalSession | None:
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
