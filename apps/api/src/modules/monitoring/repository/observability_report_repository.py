"""MonObservabilityReport repository — Phase 4."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.monitoring.domain.value_objects import PageResult
from modules.monitoring.models.observability_report import MonObservabilityReport
from modules.monitoring.repository.base import MonitoringScopedRepository, utcnow

_SORT = {
    "created_at",
    "last_generated_at",
    "report_code",
    "report_kind",
    "report_name",
    "status",
    "updated_at",
}


class ObservabilityReportRepository(MonitoringScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> MonObservabilityReport | None:
        stmt = select(MonObservabilityReport).where(
            MonObservabilityReport.id == row_id,
            MonObservabilityReport.is_deleted.is_(False),
        )
        stmt = self.apply_monitoring_filter(stmt, MonObservabilityReport, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(
        self, ctx: TenantContext, row_id: UUID
    ) -> MonObservabilityReport | None:
        stmt = select(MonObservabilityReport).where(MonObservabilityReport.id == row_id)
        stmt = self.apply_monitoring_filter(stmt, MonObservabilityReport, ctx)
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
        sort_by: str | None = "report_name",
        sort_dir: str = "asc",
        include_archived: bool = False,
        report_kind: str | None = None,
    ) -> PageResult:
        stmt = select(MonObservabilityReport).where(
            MonObservabilityReport.company_id == company_id
        )
        if not include_archived:
            stmt = stmt.where(MonObservabilityReport.is_deleted.is_(False))
        if status:
            stmt = stmt.where(MonObservabilityReport.status == status)
        if report_kind:
            stmt = stmt.where(MonObservabilityReport.report_kind == report_kind)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                MonObservabilityReport.report_name.ilike(like)
                | MonObservabilityReport.report_code.ilike(like)
            )
        stmt = self.apply_monitoring_filter(stmt, MonObservabilityReport, ctx)
        return self.paginate_sorted(
            stmt,
            MonObservabilityReport,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> MonObservabilityReport:
        row = MonObservabilityReport(
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
    ) -> MonObservabilityReport | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> MonObservabilityReport | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> MonObservabilityReport | None:
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
