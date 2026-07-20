"""NotificationService."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.vendor_portal.domain.enums import VendorPortalEntityType
from modules.vendor_portal.models import VpNotification
from modules.vendor_portal.repository.notification_repository import NotificationRepository
from modules.vendor_portal.service.engines import NotificationEngine
from modules.vendor_portal.service.vendor_portal_number_service import VendorPortalNumberService
from modules.vendor_portal.service.vendor_portal_scope_validator import VendorPortalScopeValidator


class NotificationService:
    def __init__(self, db: Session) -> None:
        self._repo = NotificationRepository(db)
        self._scope = VendorPortalScopeValidator(db)
        self._numbers = VendorPortalNumberService(db)
        self._engine = NotificationEngine()
        self._audit = AuditService(db)

    def list(self, ctx: TenantContext, company_id: UUID | None = None):
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(ctx, cid)

    def get(self, ctx: TenantContext, row_id: UUID) -> VpNotification:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("NotificationService not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)

        doc = self._numbers.generate(
            VendorPortalEntityType.NOTIFICATION,
            cid,
            VpNotification,
            "notification_number",
        )
        return self._repo.create(ctx, company_id=cid, notification_number=doc, **fields)

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        row = self._repo.update(ctx, row_id, **fields)
        if row is None:
            raise NotFoundException("NotificationService not found")
        return row

