"""DeveloperOrganizationService — Phase 1 CRUD."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.devportal.domain.value_objects import PageResult
from modules.devportal.models.developer_organization import DpDeveloperOrganization
from modules.devportal.repository.developer_organization_repository import (
    DeveloperOrganizationRepository,
)
from modules.devportal.service.devportal_scope_validator import DevportalScopeValidator
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class DeveloperOrganizationService:
    def __init__(self, db: Session) -> None:
        self._repo = DeveloperOrganizationRepository(db)
        self._scope = DevportalScopeValidator(db)
        self._audit = AuditService(db)


    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "org_name",
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

    def get(self, ctx: TenantContext, row_id: UUID) -> DpDeveloperOrganization:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("DeveloperOrganization not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)

        code = fields.pop("org_code", None) or f"ORG-{uuid4().hex[:8].upper()}"
        fields.setdefault("org_code", code)

        fields.setdefault("status", "active")

        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_developer_organization",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)

        fields.pop("status", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("DeveloperOrganization not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_developer_organization",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("DeveloperOrganization not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_developer_organization",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived DeveloperOrganization not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_developer_organization",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

