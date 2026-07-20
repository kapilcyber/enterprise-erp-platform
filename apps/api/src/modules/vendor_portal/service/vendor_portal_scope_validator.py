"""Vendor Portal scope validator."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.vendor_portal.repository.base import VendorPortalScopedRepository


class VendorPortalScopeValidator:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_company_id(self, ctx: TenantContext, company_id: UUID | None) -> UUID:
        return VendorPortalScopedRepository.resolve_company_id(ctx, company_id)

    def ensure_company_access(self, ctx: TenantContext, company_id: UUID) -> None:
        VendorPortalScopedRepository.ensure_company_access(ctx, company_id)
