"""ApplicationService — Phase 1 CRUD + lifecycle."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.devportal.adapters.integration_hub_port import DevportalIntegrationHubAdapter
from modules.devportal.domain.exceptions import HubBindingRequired
from modules.devportal.domain.value_objects import PageResult
from modules.devportal.models.application import DpApplication
from modules.devportal.repository.application_repository import ApplicationRepository
from modules.devportal.service.devportal_scope_validator import DevportalScopeValidator
from modules.devportal.service.engines import ApplicationLifecycleEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class ApplicationService:
    def __init__(self, db: Session) -> None:
        self._repo = ApplicationRepository(db)
        self._scope = DevportalScopeValidator(db)
        self._audit = AuditService(db)
        self._engine = ApplicationLifecycleEngine()
        self._hub = DevportalIntegrationHubAdapter(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "application_name",
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

    def get(self, ctx: TenantContext, row_id: UUID) -> DpApplication:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Application not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)

        code = fields.pop("application_code", None) or f"APP-{uuid4().hex[:8].upper()}"
        fields.setdefault("application_code", code)

        fields.setdefault("status", "draft")

        row = self._repo.create(ctx, company_id=cid, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_application",
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
            raise NotFoundException("Application not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_application",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Application not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_application",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived Application not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_application",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def submit(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.submit(row)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            workflow_status=getattr(row, "workflow_status", None),
        )
        if updated is None:
            raise NotFoundException("not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_application",
            entity_id=updated.id,
            operation="submit",
            performed_by=ctx.user_id,
        )
        return updated

    def approve(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.approve(row)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            workflow_status=getattr(row, "workflow_status", None),
        )
        if updated is None:
            raise NotFoundException("not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_application",
            entity_id=updated.id,
            operation="approve",
            performed_by=ctx.user_id,
        )
        return updated

    def activate(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            workflow_status=getattr(row, "workflow_status", None),
        )
        if updated is None:
            raise NotFoundException("not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_application",
            entity_id=updated.id,
            operation="activate",
            performed_by=ctx.user_id,
        )
        return updated

    def suspend(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.suspend(row)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            workflow_status=getattr(row, "workflow_status", None),
        )
        if updated is None:
            raise NotFoundException("not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_application",
            entity_id=updated.id,
            operation="suspend",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, **kwargs):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            workflow_status=getattr(row, "workflow_status", None),
        )
        if updated is None:
            raise NotFoundException("not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_application",
            entity_id=updated.id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated

    def bind_hub_refs(
        self,
        ctx: TenantContext,
        row_id: UUID,
        *,
        oauth_client_id: UUID | None = None,
        api_credential_id: UUID | None = None,
    ):
        """Bind Integration Hub UUID references only — never store secrets."""
        row = self.get(ctx, row_id)
        oauth_ref = self._hub.resolve_oauth_client_ref(ctx, oauth_client_id)
        cred_ref = self._hub.resolve_api_credential_ref(ctx, api_credential_id)
        if oauth_ref is None and cred_ref is None:
            raise HubBindingRequired(
                "At least one Hub UUID (oauth_client_id or api_credential_id) is required"
            )
        updated = self._repo.update(
            ctx,
            row_id,
            oauth_client_id=oauth_ref if oauth_ref is not None else row.oauth_client_id,
            api_credential_id=cred_ref if cred_ref is not None else row.api_credential_id,
        )
        if updated is None:
            raise NotFoundException("Application not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="dp_application",
            entity_id=updated.id,
            operation="bind_hub",
            performed_by=ctx.user_id,
        )
        return updated

