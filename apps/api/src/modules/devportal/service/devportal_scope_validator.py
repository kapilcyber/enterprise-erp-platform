"""API Developer Portal scope validator — Phase 0."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.devportal.repository.base import DevportalScopedRepository
from modules.foundation.domain.value_objects import TenantContext


class DevportalScopeValidator(DevportalScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def validate_company_access(self, ctx: TenantContext, company_id: UUID) -> None:
        self.ensure_company_access(ctx, company_id)
