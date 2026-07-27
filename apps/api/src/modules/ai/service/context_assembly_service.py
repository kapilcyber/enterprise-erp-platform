"""Context assembly — create / get context package."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.repository.context_package_repository import ContextPackageRepository
from modules.ai.service.context_package_service import ContextPackageService
from modules.ai.service.engines import ContextPackagingEngine
from modules.foundation.domain.value_objects import TenantContext


class ContextAssemblyService:
    def __init__(self, db: Session) -> None:
        self._packages = ContextPackageRepository(db)
        self._package_service = ContextPackageService(db)
        self._packaging = ContextPackagingEngine()

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        return self._package_service.create(ctx, company_id=company_id, **fields)

    def get(self, ctx: TenantContext, package_id: UUID):
        row = self._packages.get(ctx, package_id)
        if row is None:
            raise NotFoundException("Context package not found")
        return row

    def assemble(self, ctx: TenantContext, package_id: UUID) -> dict:
        package = self.get(ctx, package_id)
        return self._packaging.assemble(package)
