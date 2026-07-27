"""SkillService — Phase 3 CRUD + publish / retire."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.ai.domain.enums import AiEntityType, SkillStatus
from modules.ai.domain.json_bindings import serialize_uuid_list
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.skill import AiSkill
from modules.ai.repository.skill_repository import SkillRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import SkillEngine
from modules.ai.service.publish_validation_service import PublishValidationService
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class SkillService:
    def __init__(self, db: Session) -> None:
        self._repo = SkillRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = SkillEngine()
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
        sort_by: str | None = "skill_name",
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

    def get(self, ctx: TenantContext, row_id: UUID) -> AiSkill:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Skill not found")
        return row

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        cid = self._scope.resolve_company_id(ctx, company_id)
        code = fields.pop("skill_code", None) or self._numbers.generate(
            AiEntityType.SKILL, cid, AiSkill, "skill_code"
        )
        if "tool_version_ids" in fields:
            fields["tool_version_ids_json"] = serialize_uuid_list(
                fields.pop("tool_version_ids")
            )
        elif "tool_version_ids_json" not in fields:
            fields["tool_version_ids_json"] = "[]"
        fields.setdefault("status", SkillStatus.DRAFT.value)
        row = self._repo.create(ctx, company_id=cid, skill_code=code, **fields)
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_skill",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        if "tool_version_ids" in fields:
            fields["tool_version_ids_json"] = serialize_uuid_list(
                fields.pop("tool_version_ids")
            )
        fields.pop("status", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Skill not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_skill",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Skill not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_skill",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived skill not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_skill",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def validate_publish(self, ctx: TenantContext, row_id: UUID):
        return self._publish_validator.validate_skill(ctx, row_id)

    def publish(self, ctx: TenantContext, row_id: UUID, publish_reason: str | None = None):
        result = self._publish_validator.validate_skill(ctx, row_id)
        if not result.valid:
            raise ConflictException(
                f"Publish validation failed: {[i.code for i in result.issues]}"
            )
        row = self.get(ctx, row_id)
        self._engine.publish(row, user_id=ctx.user_id, publish_reason=publish_reason)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            published_at=row.published_at,
            published_by=row.published_by,
            publish_reason=row.publish_reason,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_skill",
            entity_id=row_id,
            operation="publish",
            performed_by=ctx.user_id,
            new_value={"publish_reason": publish_reason},
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, retire_reason: str | None = None):
        row = self.get(ctx, row_id)
        self._engine.retire(row, user_id=ctx.user_id, retire_reason=retire_reason)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            retired_at=row.retired_at,
            retired_by=row.retired_by,
            retire_reason=row.retire_reason,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_skill",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
            new_value={"retire_reason": retire_reason},
        )
        return updated
