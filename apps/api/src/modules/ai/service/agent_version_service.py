"""AgentVersionService — Phase 3 create_draft / publish / retire / clone."""

from __future__ import annotations

import builtins
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.ai.domain.enums import AgentVersionStatus, AiEntityType
from modules.ai.domain.json_bindings import serialize_uuid_list
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.agent_version import AiAgentVersion
from modules.ai.repository.agent_repository import AgentRepository
from modules.ai.repository.agent_version_repository import AgentVersionRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import AgentOrchestrationLimitsEngine, AgentVersionEngine
from modules.ai.service.publish_validation_service import PublishValidationService
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class AgentVersionService:
    def __init__(self, db: Session) -> None:
        self._repo = AgentVersionRepository(db)
        self._agents = AgentRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = AgentVersionEngine()
        self._audit = AuditService(db)
        self._publish_validator = PublishValidationService(db)
        self._limits_engine = AgentOrchestrationLimitsEngine()

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
        agent_id: UUID | None = None,
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
            agent_id=agent_id,
        )

    def list_by_agent(self, ctx: TenantContext, agent_id: UUID):
        if self._agents.get(ctx, agent_id) is None:
            raise NotFoundException("Agent not found")
        return self._repo.list_by_agent(ctx, agent_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiAgentVersion:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Agent version not found")
        return row

    def create_draft(
        self,
        ctx: TenantContext,
        agent_id: UUID,
        *,
        prompt_version_id: UUID,
        skill_ids: builtins.list[UUID] | None = None,
        tool_version_ids: builtins.list[UUID] | None = None,
        knowledge_base_id: UUID | None = None,
        gateway_policy_id: UUID | None = None,
        guardrail_policy_id: UUID | None = None,
        moderation_policy_id: UUID | None = None,
        rate_limit_policy_id: UUID | None = None,
        bpm_definition_id: UUID | None = None,
        max_steps: int | None = None,
        max_tokens: int | None = None,
        hitl_policy_json: str | None = None,
        orchestration_limits_json: str | None = None,
        version_label: str | None = None,
        company_id: UUID | None = None,
    ):
        agent = self._agents.get(ctx, agent_id)
        if agent is None:
            raise NotFoundException("Agent not found")
        self._limits_engine.assert_valid(max_steps=max_steps, max_tokens=max_tokens)
        cid = self._scope.resolve_company_id(ctx, company_id or agent.company_id)
        version_number = self._repo.next_version_number(ctx, agent_id)
        ver_code = self._numbers.generate(
            AiEntityType.AGENT_VERSION, cid, AiAgentVersion, "version_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            agent_id=agent_id,
            version_code=ver_code,
            version_number=version_number,
            version_label=version_label or f"v{version_number}",
            prompt_version_id=prompt_version_id,
            skill_ids_json=serialize_uuid_list(skill_ids),
            tool_version_ids_json=serialize_uuid_list(tool_version_ids),
            knowledge_base_id=knowledge_base_id,
            gateway_policy_id=gateway_policy_id,
            guardrail_policy_id=guardrail_policy_id,
            moderation_policy_id=moderation_policy_id,
            rate_limit_policy_id=rate_limit_policy_id,
            bpm_definition_id=bpm_definition_id,
            max_steps=max_steps,
            max_tokens=max_tokens,
            hitl_policy_json=hitl_policy_json,
            orchestration_limits_json=orchestration_limits_json,
            status=AgentVersionStatus.DRAFT.value,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_agent_version",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        if "skill_ids" in fields:
            fields["skill_ids_json"] = serialize_uuid_list(fields.pop("skill_ids"))
        if "tool_version_ids" in fields:
            fields["tool_version_ids_json"] = serialize_uuid_list(
                fields.pop("tool_version_ids")
            )
        max_steps = fields.get("max_steps", row.max_steps)
        max_tokens = fields.get("max_tokens", row.max_tokens)
        if "max_steps" in fields or "max_tokens" in fields:
            self._limits_engine.assert_valid(max_steps=max_steps, max_tokens=max_tokens)
        fields.pop("status", None)
        fields.pop("agent_id", None)
        fields.pop("version_number", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Agent version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_agent_version",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Agent version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_agent_version",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived agent version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_agent_version",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def validate_publish(self, ctx: TenantContext, row_id: UUID):
        return self._publish_validator.validate_agent_version(ctx, row_id)

    def publish(self, ctx: TenantContext, row_id: UUID, *, publish_reason: str | None = None):
        result = self._publish_validator.validate_agent_version(ctx, row_id)
        if not result.valid:
            raise ConflictException(
                f"Publish validation failed: {[i.code for i in result.issues]}"
            )
        row = self.get(ctx, row_id)
        prior = self._repo.get_published(ctx, row.agent_id)
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
            entity_name="ai_agent_version",
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
            entity_name="ai_agent_version",
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
        version_number = self._repo.next_version_number(ctx, source.agent_id)
        ver_code = self._numbers.generate(
            AiEntityType.AGENT_VERSION, cid, AiAgentVersion, "version_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            agent_id=source.agent_id,
            version_code=ver_code,
            version_number=version_number,
            version_label=version_label or f"v{version_number}",
            prompt_version_id=source.prompt_version_id,
            skill_ids_json=source.skill_ids_json,
            tool_version_ids_json=source.tool_version_ids_json,
            knowledge_base_id=source.knowledge_base_id,
            gateway_policy_id=source.gateway_policy_id,
            guardrail_policy_id=source.guardrail_policy_id,
            moderation_policy_id=source.moderation_policy_id,
            rate_limit_policy_id=source.rate_limit_policy_id,
            bpm_definition_id=source.bpm_definition_id,
            max_steps=source.max_steps,
            max_tokens=source.max_tokens,
            hitl_policy_json=source.hitl_policy_json,
            orchestration_limits_json=source.orchestration_limits_json,
            status=AgentVersionStatus.DRAFT.value,
            cloned_from_version_id=source.id,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_agent_version",
            entity_id=row.id,
            operation="clone",
            performed_by=ctx.user_id,
            new_value={"source_id": str(source.id), "clone_reason": clone_reason},
        )
        return row
