"""PromptVersionService — Phase 1 publish / retire / clone."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.ai.domain.enums import AiEntityType, PromptVersionStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.prompt_version import AiPromptVersion
from modules.ai.repository.prompt_template_repository import PromptTemplateRepository
from modules.ai.repository.prompt_version_repository import PromptVersionRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import PromptVersionEngine
from modules.ai.service.publish_validation_service import PublishValidationService
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class PromptVersionService:
    def __init__(self, db: Session) -> None:
        self._repo = PromptVersionRepository(db)
        self._templates = PromptTemplateRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = PromptVersionEngine()
        self._audit = AuditService(db)
        self._publish_validator = PublishValidationService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "version_number",
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

    def list_by_template(self, ctx: TenantContext, template_id: UUID):
        if self._templates.get(ctx, template_id) is None:
            raise NotFoundException("Prompt template not found")
        return self._repo.list_by_template(ctx, template_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiPromptVersion:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Prompt version not found")
        return row

    def create_draft(
        self,
        ctx: TenantContext,
        template_id: UUID,
        *,
        content_text: str,
        version_label: str | None = None,
        change_notes: str | None = None,
        company_id: UUID | None = None,
    ):
        template = self._templates.get(ctx, template_id)
        if template is None:
            raise NotFoundException("Prompt template not found")
        cid = self._scope.resolve_company_id(ctx, company_id or template.company_id)
        version_number = self._repo.next_version_number(ctx, template_id)
        ver_code = self._numbers.generate(
            AiEntityType.PROMPT_VERSION, cid, AiPromptVersion, "version_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            template_id=template_id,
            version_code=ver_code,
            version_number=version_number,
            version_label=version_label or f"v{version_number}",
            change_notes=change_notes,
            content_text=content_text,
            status=PromptVersionStatus.DRAFT.value,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_prompt_version",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        fields.pop("status", None)
        fields.pop("template_id", None)
        fields.pop("version_number", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Prompt version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_prompt_version",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Prompt version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_prompt_version",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived prompt version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_prompt_version",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def validate_publish(self, ctx: TenantContext, row_id: UUID):
        return self._publish_validator.validate_prompt_version(ctx, row_id)

    def publish(self, ctx: TenantContext, row_id: UUID, *, publish_reason: str | None = None):
        result = self._publish_validator.validate_prompt_version(ctx, row_id)
        if not result.valid:
            raise ConflictException(
                f"Publish validation failed: {[i.code for i in result.issues]}"
            )
        row = self.get(ctx, row_id)
        prior = self._repo.get_published(ctx, row.template_id)
        if prior is not None and prior.id != row.id:
            self._engine.retire_published(prior, user_id=ctx.user_id)
            self._repo.update(
                ctx,
                prior.id,
                status=prior.status,
                retired_at=prior.retired_at,
                retired_by=prior.retired_by,
                retire_reason="Auto-retired: superseded by publish",
            )
        self._engine.publish(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            published_at=row.published_at,
            published_by=row.published_by,
            publish_reason=publish_reason,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_prompt_version",
            entity_id=row_id,
            operation="publish",
            performed_by=ctx.user_id,
            new_value={"publish_reason": publish_reason},
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, *, retire_reason: str | None = None):
        row = self.get(ctx, row_id)
        self._engine.retire(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            retired_at=row.retired_at,
            retired_by=row.retired_by,
            retire_reason=retire_reason,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_prompt_version",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
            new_value={"retire_reason": retire_reason},
        )
        return updated

    def clone_version(
        self,
        ctx: TenantContext,
        row_id: UUID,
        *,
        version_label: str | None = None,
        change_notes: str | None = None,
        clone_reason: str | None = None,
    ):
        source = self.get(ctx, row_id)
        cid = source.company_id
        version_number = self._repo.next_version_number(ctx, source.template_id)
        ver_code = self._numbers.generate(
            AiEntityType.PROMPT_VERSION, cid, AiPromptVersion, "version_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            template_id=source.template_id,
            version_code=ver_code,
            version_number=version_number,
            version_label=version_label or f"v{version_number}",
            change_notes=change_notes or f"Cloned from version {source.version_number}",
            content_text=source.content_text,
            status=PromptVersionStatus.DRAFT.value,
            cloned_from_version_id=source.id,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_prompt_version",
            entity_id=row.id,
            operation="clone",
            performed_by=ctx.user_id,
            new_value={"source_id": str(source.id), "clone_reason": clone_reason},
        )
        return row
