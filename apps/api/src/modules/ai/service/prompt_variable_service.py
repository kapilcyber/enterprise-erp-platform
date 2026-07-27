"""PromptVariableService — Phase 1 CRUD (draft version only)."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import AiEntityType
from modules.ai.models.prompt_variable import AiPromptVariable
from modules.ai.repository.prompt_variable_repository import PromptVariableRepository
from modules.ai.repository.prompt_version_repository import PromptVersionRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import PromptVariableEngine
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class PromptVariableService:
    def __init__(self, db: Session) -> None:
        self._repo = PromptVariableRepository(db)
        self._versions = PromptVersionRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = PromptVariableEngine()
        self._audit = AuditService(db)

    def list_by_version(self, ctx: TenantContext, prompt_version_id: UUID):
        version = self._versions.get(ctx, prompt_version_id)
        if version is None:
            raise NotFoundException("Prompt version not found")
        return self._repo.list_by_version(ctx, prompt_version_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiPromptVariable:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Prompt variable not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        prompt_version_id = fields.get("prompt_version_id")
        version = self._versions.get(ctx, prompt_version_id) if prompt_version_id else None
        if version is None:
            raise NotFoundException("Prompt version not found")
        self._engine.assert_editable_on_draft_version(version.status)
        cid = self._scope.resolve_company_id(ctx, company_id or version.company_id)
        code = fields.pop("variable_code", None) or self._numbers.generate(
            AiEntityType.PROMPT_VARIABLE, cid, AiPromptVariable, "variable_code"
        )
        row = self._repo.create(ctx, company_id=cid, variable_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_prompt_variable",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        version = self._versions.get(ctx, row.prompt_version_id)
        if version is None:
            raise NotFoundException("Prompt version not found")
        self._engine.assert_editable_on_draft_version(version.status)
        fields.pop("prompt_version_id", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Prompt variable not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_prompt_variable",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self.get(ctx, row_id)
        version = self._versions.get(ctx, row.prompt_version_id)
        if version is None:
            raise NotFoundException("Prompt version not found")
        self._engine.assert_editable_on_draft_version(version.status)
        archived = self._repo.soft_delete(ctx, row_id)
        if archived is None:
            raise NotFoundException("Prompt variable not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_prompt_variable",
            entity_id=archived.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return archived
