"""ObservabilityReportService — Phase 4 CRUD + lifecycle."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.monitoring.domain.enums import REPORT_KIND_VALUES
from modules.monitoring.domain.value_objects import PageResult
from modules.monitoring.repository.observability_report_repository import (
    ObservabilityReportRepository,
)
from modules.monitoring.service.engines import ObservabilityReportLifecycleEngine
from modules.monitoring.service.monitoring_scope_validator import MonitoringScopeValidator


class ObservabilityReportService:
    def __init__(self, db: Session) -> None:
        self._repo = ObservabilityReportRepository(db)
        self._scope = MonitoringScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = ObservabilityReportLifecycleEngine()

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
        report_kind: str | None = None,
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
            report_kind=report_kind,
        )

    def get(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("ObservabilityReport not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        report_kind = fields.get("report_kind") or "operational"
        if report_kind not in REPORT_KIND_VALUES:
            raise ConflictException("Invalid report_kind")
        fields["report_kind"] = report_kind
        code = fields.pop("report_code", None) or f"RPT-{uuid4().hex[:8].upper()}"
        fields.setdefault("report_code", code)
        fields.setdefault("status", "draft")
        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_report",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        fields.pop("status", None)
        if "report_kind" in fields and fields["report_kind"] is not None and (
            fields["report_kind"] not in REPORT_KIND_VALUES
        ):
            raise ConflictException("Invalid report_kind")
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("ObservabilityReport not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_report",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("ObservabilityReport not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_report",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived ObservabilityReport not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_report",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def activate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("ObservabilityReport not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_report",
            entity_id=updated.id,
            operation="activate",
            performed_by=ctx.user_id,
        )
        return updated

    def mark_archived(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.mark_archived(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        if updated is None:
            raise NotFoundException("ObservabilityReport not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="mon_observability_report",
            entity_id=updated.id,
            operation="mark_archived",
            performed_by=ctx.user_id,
        )
        return updated
