"""ProviderCredentialReferenceService — Phase 1 CRUD + lifecycle."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType, CredentialReferenceStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.provider_credential_reference import AiProviderCredentialReference
from modules.ai.repository.provider_credential_reference_repository import (
    ProviderCredentialReferenceRepository,
)
from modules.ai.repository.provider_repository import ProviderRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import CredentialReferenceEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class ProviderCredentialReferenceService:
    def __init__(self, db: Session) -> None:
        self._repo = ProviderCredentialReferenceRepository(db)
        self._providers = ProviderRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = CredentialReferenceEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        provider_id: UUID | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "credential_code",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            provider_id=provider_id,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiProviderCredentialReference:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Provider credential reference not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        provider_id = fields.get("provider_id")
        if provider_id and self._providers.get(ctx, provider_id) is None:
            raise NotFoundException("AI provider not found")
        code = fields.pop("credential_code", None) or self._numbers.generate(
            AiEntityType.PROVIDER_CREDENTIAL_REFERENCE,
            cid,
            AiProviderCredentialReference,
            "credential_code",
        )
        fields.setdefault("status", CredentialReferenceStatus.ACTIVE.value)
        row = self._repo.create(ctx, company_id=cid, credential_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_provider_credential_reference",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        self.get(ctx, row_id)
        fields.pop("status", None)
        row = self._repo.update(ctx, row_id, **fields)
        if row is None:
            raise NotFoundException("Provider credential reference not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_provider_credential_reference",
            entity_id=row.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return row

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Provider credential reference not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_provider_credential_reference",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived credential reference not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_provider_credential_reference",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def activate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.activate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_provider_credential_reference",
            entity_id=row_id,
            operation="activate",
            performed_by=ctx.user_id,
        )
        return updated

    def rotate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.rotate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_provider_credential_reference",
            entity_id=row_id,
            operation="rotate",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_provider_credential_reference",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
