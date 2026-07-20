"""ReportService."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.vendor_portal.models import VpReport
from modules.vendor_portal.repository.report_repository import ReportRepository
from modules.vendor_portal.service.engines import ReportEngine
from modules.vendor_portal.service.vendor_portal_scope_validator import VendorPortalScopeValidator


class ReportService:
    def __init__(self, db: Session) -> None:
        self._repo = ReportRepository(db)
        self._scope = VendorPortalScopeValidator(db)
        self._engine = ReportEngine()
        self._audit = AuditService(db)

    def list(self, ctx: TenantContext, company_id: UUID | None = None):
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(ctx, cid)

    def get(self, ctx: TenantContext, row_id: UUID) -> VpReport:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("ReportService not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)

        return self._repo.create(ctx, company_id=cid, **fields)

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        row = self._repo.update(ctx, row_id, **fields)
        if row is None:
            raise NotFoundException("ReportService not found")
        return row

