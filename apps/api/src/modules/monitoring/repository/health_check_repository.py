"""MonHealthCheck repository — Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.monitoring.domain.value_objects import PageResult
from modules.monitoring.models.health_check import MonHealthCheck
from modules.monitoring.repository.base import MonitoringScopedRepository, utcnow

_SORT = {"check_code", "check_kind", "check_name", "created_at", "status", "updated_at"}


class HealthCheckRepository(MonitoringScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> MonHealthCheck | None:
        stmt = select(MonHealthCheck).where(
            MonHealthCheck.id == row_id,
            MonHealthCheck.is_deleted.is_(False),
        )
        stmt = self.apply_monitoring_filter(stmt, MonHealthCheck, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> MonHealthCheck | None:
        stmt = select(MonHealthCheck).where(MonHealthCheck.id == row_id)
        stmt = self.apply_monitoring_filter(stmt, MonHealthCheck, ctx)
        return self.db.scalar(stmt)

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
        *,
        status: str | None = None,
        search: str | None = None,
        service_id: UUID | None = None,
        component_id: UUID | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "check_name",
        sort_dir: str = "asc",
        include_archived: bool = False,
    ) -> PageResult:
        stmt = select(MonHealthCheck).where(MonHealthCheck.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(MonHealthCheck.is_deleted.is_(False))
        if status:
            stmt = stmt.where(MonHealthCheck.status == status)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                MonHealthCheck.check_name.ilike(like) |
                MonHealthCheck.check_code.ilike(like)
            )

        if service_id:
            stmt = stmt.where(MonHealthCheck.service_id == service_id)

        if component_id:
            stmt = stmt.where(MonHealthCheck.component_id == component_id)
        stmt = self.apply_monitoring_filter(stmt, MonHealthCheck, ctx)
        return self.paginate_sorted(
            stmt,
            MonHealthCheck,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> MonHealthCheck:
        row = MonHealthCheck(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> MonHealthCheck | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> MonHealthCheck | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> MonHealthCheck | None:
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
