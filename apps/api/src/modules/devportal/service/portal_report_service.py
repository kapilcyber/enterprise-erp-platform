"""PortalReportService — Phase 4 operational report metadata; Hub projection via contract."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.devportal.adapters.analytics_port import DevportalAnalyticsAdapter
from modules.devportal.adapters.integration_hub_port import DevportalIntegrationHubAdapter
from modules.devportal.domain.value_objects import PageResult
from modules.devportal.models.portal_report import DpPortalReport
from modules.devportal.repository.portal_report_repository import PortalReportRepository
from modules.devportal.service.devportal_scope_validator import DevportalScopeValidator
from modules.devportal.service.engines import PortalReportEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class PortalReportService:
    def __init__(self, db: Session) -> None:
        self._repo = PortalReportRepository(db)
        self._scope = DevportalScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = PortalReportEngine()
        self._hub = DevportalIntegrationHubAdapter(db)
        self._analytics = DevportalAnalyticsAdapter(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "report_name",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> DpPortalReport:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("PortalReport not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        report_type = fields.get("report_type")
        if not isinstance(report_type, str):
            raise ConflictException("report_type is required")
        self._engine.assert_report_type(report_type)
        analytics_id = self._analytics.resolve_report_ref(
            ctx, fields.get("analytics_report_id")
        )
        fields["analytics_report_id"] = analytics_id
        code = fields.pop("report_code", None) or f"RPT-{uuid4().hex[:8].upper()}"
        fields.setdefault("report_code", code)
        fields.setdefault("status", "draft")
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_portal_report",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        fields.pop("status", None)
        if "report_type" in fields and fields["report_type"] is not None:
            self._engine.assert_report_type(fields["report_type"])
        if "analytics_report_id" in fields:
            fields["analytics_report_id"] = self._analytics.resolve_report_ref(
                ctx, fields.get("analytics_report_id")
            )
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("PortalReport not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_portal_report",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("PortalReport not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_portal_report",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived PortalReport not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_portal_report",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def finalize(self, ctx: TenantContext, row_id: UUID, **kwargs):
        _ = kwargs
        row = self.get(ctx, row_id)
        snapshot = self._hub.project_usage_metrics(
            ctx,
            report_type=row.report_type,
            period_start=row.period_start,
            period_end=row.period_end,
            filters=row.filters_json,
        )
        self._engine.finalize(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            finalized_at=row.finalized_at,
            finalized_by=row.finalized_by,
            projection_snapshot_json=snapshot,
            projected_at=datetime.now(timezone.utc),
        )
        if updated is None:
            raise NotFoundException("PortalReport not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_portal_report",
            entity_id=updated.id,
            operation="finalize",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        _ = kwargs
        row = self.get(ctx, row_id)
        self._engine.retire(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            retired_at=row.retired_at,
            retired_by=row.retired_by,
        )
        if updated is None:
            raise NotFoundException("PortalReport not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_portal_report",
            entity_id=updated.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated

    def export(self, ctx: TenantContext, row_id: UUID, **kwargs):
        _ = kwargs
        row = self.get(ctx, row_id)
        self._engine.assert_exportable(row)
        self._engine.assert_projection_freshness(row)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_portal_report",
            entity_id=row.id,
            operation="export",
            performed_by=ctx.user_id,
        )
        return row
