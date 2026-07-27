"""ModelService — Phase 1 CRUD + lifecycle."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType, ModelStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.ai_model import AiModel
from modules.ai.repository.model_repository import ModelRepository
from modules.ai.repository.provider_repository import ProviderRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import ModelEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class ModelService:
    def __init__(self, db: Session) -> None:
        self._repo = ModelRepository(db)
        self._providers = ProviderRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = ModelEngine()
        self._audit = AuditService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        provider_id: UUID | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "model_name",
        sort_dir: str = "asc",
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            provider_id=provider_id,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
        )

    def get(self, ctx: TenantContext, row_id: UUID) -> AiModel:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("AI model not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        provider_id = fields.get("provider_id")
        if provider_id and self._providers.get(ctx, provider_id) is None:
            raise NotFoundException("AI provider not found")
        code = fields.pop("model_code", None) or self._numbers.generate(
            AiEntityType.MODEL, cid, AiModel, "model_code"
        )
        fields.setdefault("status", ModelStatus.DRAFT.value)
        row = self._repo.create(ctx, company_id=cid, model_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_model",
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
            raise NotFoundException("AI model not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_model",
            entity_id=row.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return row

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("AI model not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_model",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived AI model not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_model",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def approve(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.approve(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_model",
            entity_id=row_id,
            operation="approve",
            performed_by=ctx.user_id,
        )
        return updated

    def deprecate(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.deprecate(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_model",
            entity_id=row_id,
            operation="deprecate",
            performed_by=ctx.user_id,
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        self._engine.retire(row)
        updated = self._repo.update(ctx, row_id, status=row.status)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_model",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
        )
        return updated
