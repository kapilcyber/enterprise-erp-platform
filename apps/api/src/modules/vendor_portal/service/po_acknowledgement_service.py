"""PoAcknowledgementService."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.vendor_portal.domain.enums import VendorPortalEntityType
from modules.vendor_portal.models import VpPoAcknowledgement
from modules.vendor_portal.repository.po_acknowledgement_repository import (
    PoAcknowledgementRepository,
)
from modules.vendor_portal.service.engines import PoAcknowledgementEngine
from modules.vendor_portal.service.vendor_portal_number_service import VendorPortalNumberService
from modules.vendor_portal.service.vendor_portal_scope_validator import VendorPortalScopeValidator


class PoAcknowledgementService:
    def __init__(self, db: Session) -> None:
        self._repo = PoAcknowledgementRepository(db)
        self._scope = VendorPortalScopeValidator(db)
        self._numbers = VendorPortalNumberService(db)
        self._engine = PoAcknowledgementEngine()
        self._audit = AuditService(db)

    def list(self, ctx: TenantContext, company_id: UUID | None = None):
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(ctx, cid)

    def get(self, ctx: TenantContext, row_id: UUID) -> VpPoAcknowledgement:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("PoAcknowledgementService not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)

        doc = self._numbers.generate(
            VendorPortalEntityType.PO_ACKNOWLEDGEMENT,
            cid,
            VpPoAcknowledgement,
            "ack_number",
        )
        return self._repo.create(ctx, company_id=cid, ack_number=doc, **fields)

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        row = self._repo.update(ctx, row_id, **fields)
        if row is None:
            raise NotFoundException("PoAcknowledgementService not found")
        return row

    def submit(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.submit(row)
        return self._repo.update(ctx, row_id, status=row.status)

    def approve(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.approve(row)
        return self._repo.update(ctx, row_id, status=row.status)

