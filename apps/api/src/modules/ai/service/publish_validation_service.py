"""Publish validation — prompt version and assistant publish gates."""

from dataclasses import dataclass, field
from typing import cast
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.ai.domain.enums import (
    AgentStatus,
    AgentVersionStatus,
    KnowledgeBaseStatus,
    KnowledgeSourceStatus,
    PolicyStatus,
    PromptVersionStatus,
    SkillStatus,
    ToolVersionStatus,
)
from modules.ai.domain.json_bindings import parse_uuid_list
from modules.ai.domain.value_objects import PublishValidationResult, ValidationIssue
from modules.ai.repository.agent_repository import AgentRepository
from modules.ai.repository.agent_version_repository import AgentVersionRepository
from modules.ai.repository.assistant_repository import AssistantRepository
from modules.ai.repository.gateway_policy_repository import GatewayPolicyRepository
from modules.ai.repository.guardrail_policy_repository import GuardrailPolicyRepository
from modules.ai.repository.knowledge_base_repository import KnowledgeBaseRepository
from modules.ai.repository.knowledge_source_repository import KnowledgeSourceRepository
from modules.ai.repository.moderation_policy_repository import ModerationPolicyRepository
from modules.ai.repository.prompt_template_repository import PromptTemplateRepository
from modules.ai.repository.prompt_version_repository import PromptVersionRepository
from modules.ai.repository.rate_limit_policy_repository import RateLimitPolicyRepository
from modules.ai.repository.skill_repository import SkillRepository
from modules.ai.repository.tool_version_repository import ToolVersionRepository
from modules.ai.service.engines import (
    AgentOrchestrationLimitsEngine,
    ToolAllowListEngine,
    ToolSchemaValidationEngine,
)
from modules.foundation.domain.value_objects import TenantContext


@dataclass
class AssistantPublishValidationResult:
    valid: bool
    assistant_id: UUID
    issues: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)


@dataclass
class KnowledgeBasePublishValidationResult:
    valid: bool
    knowledge_base_id: UUID
    issues: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)


@dataclass
class SkillPublishValidationResult:
    valid: bool
    skill_id: UUID
    issues: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)


@dataclass
class AgentVersionPublishValidationResult:
    valid: bool
    agent_version_id: UUID
    agent_id: UUID
    issues: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)


class PublishValidationService:
    def __init__(self, db: Session) -> None:
        self._prompt_versions = PromptVersionRepository(db)
        self._prompt_templates = PromptTemplateRepository(db)
        self._assistants = AssistantRepository(db)
        self._gateway_policies = GatewayPolicyRepository(db)
        self._guardrail_policies = GuardrailPolicyRepository(db)
        self._moderation_policies = ModerationPolicyRepository(db)
        self._rate_limit_policies = RateLimitPolicyRepository(db)
        self._knowledge_bases = KnowledgeBaseRepository(db)
        self._knowledge_sources = KnowledgeSourceRepository(db)
        self._tool_versions = ToolVersionRepository(db)
        self._skills = SkillRepository(db)
        self._agents = AgentRepository(db)
        self._agent_versions = AgentVersionRepository(db)
        self._allowlist_engine = ToolAllowListEngine()
        self._schema_engine = ToolSchemaValidationEngine()
        self._limits_engine = AgentOrchestrationLimitsEngine()

    def validate(self, ctx: TenantContext, row_id: UUID) -> PublishValidationResult:
        return self.validate_prompt_version(ctx, row_id)

    def validate_prompt_version(
        self, ctx: TenantContext, row_id: UUID
    ) -> PublishValidationResult:
        row = self._prompt_versions.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Prompt version not found")
        issues: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []
        template = self._prompt_templates.get(ctx, row.template_id)
        if template is None:
            issues.append(
                ValidationIssue(code="TEMPLATE_NOT_FOUND", message="Prompt template not found")
            )
        if row.status != PromptVersionStatus.DRAFT.value:
            issues.append(
                ValidationIssue(
                    code="NOT_DRAFT",
                    message=f"Only draft prompt versions can be published (status={row.status})",
                )
            )
        return PublishValidationResult(
            valid=len(issues) == 0,
            version_id=row.id,
            definition_id=row.template_id,
            issues=issues,
            warnings=warnings,
        )

    def validate_assistant(
        self, ctx: TenantContext, assistant_id: UUID
    ) -> AssistantPublishValidationResult:
        assistant = self._assistants.get(ctx, assistant_id)
        if assistant is None:
            raise NotFoundException("Assistant not found")
        issues: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []

        prompt_version = self._prompt_versions.get(ctx, assistant.prompt_version_id)
        if prompt_version is None:
            issues.append(
                ValidationIssue(
                    code="PROMPT_VERSION_NOT_FOUND",
                    message="Linked prompt version not found",
                )
            )
        elif prompt_version.status != PromptVersionStatus.PUBLISHED.value:
            issues.append(
                ValidationIssue(
                    code="PROMPT_VERSION_NOT_PUBLISHED",
                    message="Assistant publish requires a published prompt version",
                )
            )

        if assistant.gateway_policy_id:
            policy = self._gateway_policies.get(ctx, assistant.gateway_policy_id)
            if policy is None:
                issues.append(
                    ValidationIssue(
                        code="GATEWAY_POLICY_NOT_FOUND",
                        message="Linked gateway policy not found",
                    )
                )
            elif policy.status != PolicyStatus.PUBLISHED.value:
                issues.append(
                    ValidationIssue(
                        code="GATEWAY_POLICY_NOT_PUBLISHED",
                        message="Linked gateway policy must be published",
                    )
                )

        if assistant.guardrail_policy_id:
            policy = self._guardrail_policies.get(ctx, assistant.guardrail_policy_id)
            if policy is None:
                issues.append(
                    ValidationIssue(
                        code="GUARDRAIL_POLICY_NOT_FOUND",
                        message="Linked guardrail policy not found",
                    )
                )
            elif policy.status != PolicyStatus.PUBLISHED.value:
                issues.append(
                    ValidationIssue(
                        code="GUARDRAIL_POLICY_NOT_PUBLISHED",
                        message="Linked guardrail policy must be published",
                    )
                )

        if assistant.moderation_policy_id:
            policy = self._moderation_policies.get(ctx, assistant.moderation_policy_id)
            if policy is None:
                issues.append(
                    ValidationIssue(
                        code="MODERATION_POLICY_NOT_FOUND",
                        message="Linked moderation policy not found",
                    )
                )
            elif policy.status != PolicyStatus.PUBLISHED.value:
                issues.append(
                    ValidationIssue(
                        code="MODERATION_POLICY_NOT_PUBLISHED",
                        message="Linked moderation policy must be published",
                    )
                )

        if assistant.rate_limit_policy_id:
            policy = self._rate_limit_policies.get(ctx, assistant.rate_limit_policy_id)
            if policy is None:
                issues.append(
                    ValidationIssue(
                        code="RATE_LIMIT_POLICY_NOT_FOUND",
                        message="Linked rate limit policy not found",
                    )
                )
            elif policy.status != PolicyStatus.PUBLISHED.value:
                issues.append(
                    ValidationIssue(
                        code="RATE_LIMIT_POLICY_NOT_PUBLISHED",
                        message="Linked rate limit policy must be published",
                    )
                )

        return AssistantPublishValidationResult(
            valid=len(issues) == 0,
            assistant_id=assistant.id,
            issues=issues,
            warnings=warnings,
        )

    def validate_knowledge_base(
        self, ctx: TenantContext, knowledge_base_id: UUID
    ) -> KnowledgeBasePublishValidationResult:
        kb = self._knowledge_bases.get(ctx, knowledge_base_id)
        if kb is None:
            raise NotFoundException("Knowledge base not found")
        issues: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []

        if kb.status != KnowledgeBaseStatus.DRAFT.value:
            issues.append(
                ValidationIssue(
                    code="NOT_DRAFT",
                    message=f"Only draft knowledge bases can be published (status={kb.status})",
                )
            )

        sources = self._knowledge_sources.list_by_knowledge_base(ctx, knowledge_base_id)
        active_sources = [s for s in sources if s.status == KnowledgeSourceStatus.ACTIVE.value]
        if not active_sources:
            warnings.append(
                ValidationIssue(
                    code="NO_ACTIVE_SOURCES",
                    message="No active knowledge sources linked; publish allowed with warning",
                )
            )

        return KnowledgeBasePublishValidationResult(
            valid=len(issues) == 0,
            knowledge_base_id=kb.id,
            issues=issues,
            warnings=warnings,
        )

    def validate_tool_version(
        self, ctx: TenantContext, row_id: UUID
    ) -> PublishValidationResult:
        row = self._tool_versions.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Tool version not found")
        issues: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []
        if row.status != ToolVersionStatus.DRAFT.value:
            issues.append(
                ValidationIssue(
                    code="NOT_DRAFT",
                    message=f"Only draft tool versions can be published (status={row.status})",
                )
            )
        schema_result = self._schema_engine.validate_input_schema(row.input_schema_json)
        for item in schema_result.get("issues", []):
            issues.append(
                ValidationIssue(
                    code=item.get("code", "INPUT_SCHEMA_INVALID"),
                    message=item.get("message", "Input schema validation failed"),
                    field=item.get("field"),
                )
            )
        return PublishValidationResult(
            valid=len(issues) == 0,
            version_id=row.id,
            definition_id=row.tool_id,
            issues=issues,
            warnings=warnings,
        )

    def validate_skill(self, ctx: TenantContext, skill_id: UUID) -> SkillPublishValidationResult:
        skill = self._skills.get(ctx, skill_id)
        if skill is None:
            raise NotFoundException("Skill not found")
        issues: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []
        if skill.status != SkillStatus.DRAFT.value:
            issues.append(
                ValidationIssue(
                    code="NOT_DRAFT",
                    message=f"Only draft skills can be published (status={skill.status})",
                )
            )
        tool_version_ids = parse_uuid_list(skill.tool_version_ids_json)
        if tool_version_ids:
            lookup = cast(
                dict[UUID, object],
                {
                    tv_id: self._tool_versions.get(ctx, tv_id)
                    for tv_id in tool_version_ids
                },
            )
            allow_result = self._allowlist_engine.validate_allow_list(
                tool_version_ids, published_lookup=lookup
            )
            for item in allow_result.get("issues", []):
                issues.append(
                    ValidationIssue(
                        code=item["code"],
                        message=f"Tool version binding invalid: {item.get('tool_version_id')}",
                    )
                )
        else:
            warnings.append(
                ValidationIssue(
                    code="NO_TOOL_BINDINGS",
                    message="Skill has no tool version bindings",
                    severity="warning",
                )
            )
        if skill.prompt_version_id:
            pv = self._prompt_versions.get(ctx, skill.prompt_version_id)
            if pv is None:
                issues.append(
                    ValidationIssue(
                        code="PROMPT_VERSION_NOT_FOUND",
                        message="Linked prompt version not found",
                    )
                )
            elif pv.status != PromptVersionStatus.PUBLISHED.value:
                warnings.append(
                    ValidationIssue(
                        code="PROMPT_VERSION_NOT_PUBLISHED",
                        message="Linked prompt version is not published",
                        severity="warning",
                    )
                )
        return SkillPublishValidationResult(
            valid=len(issues) == 0,
            skill_id=skill.id,
            issues=issues,
            warnings=warnings,
        )

    def validate_agent_version(
        self, ctx: TenantContext, agent_version_id: UUID
    ) -> AgentVersionPublishValidationResult:
        av = self._agent_versions.get(ctx, agent_version_id)
        if av is None:
            raise NotFoundException("Agent version not found")
        issues: list[ValidationIssue] = []
        warnings: list[ValidationIssue] = []

        agent = self._agents.get(ctx, av.agent_id)
        if agent is None:
            issues.append(
                ValidationIssue(code="AGENT_NOT_FOUND", message="Parent agent not found")
            )
        elif agent.status != AgentStatus.ACTIVE.value:
            issues.append(
                ValidationIssue(
                    code="AGENT_NOT_ACTIVE",
                    message="Agent catalog must be active to publish a version",
                )
            )

        if av.status != AgentVersionStatus.DRAFT.value:
            issues.append(
                ValidationIssue(
                    code="NOT_DRAFT",
                    message=f"Only draft agent versions can be published (status={av.status})",
                )
            )

        prompt_version = self._prompt_versions.get(ctx, av.prompt_version_id)
        if prompt_version is None:
            issues.append(
                ValidationIssue(
                    code="PROMPT_VERSION_NOT_FOUND",
                    message="Linked prompt version not found",
                )
            )
        elif prompt_version.status != PromptVersionStatus.PUBLISHED.value:
            issues.append(
                ValidationIssue(
                    code="PROMPT_VERSION_NOT_PUBLISHED",
                    message="Agent version publish requires a published prompt version",
                )
            )

        tool_version_ids = parse_uuid_list(av.tool_version_ids_json)
        if tool_version_ids:
            lookup = cast(
                dict[UUID, object],
                {
                    tv_id: self._tool_versions.get(ctx, tv_id)
                    for tv_id in tool_version_ids
                },
            )
            allow_result = self._allowlist_engine.validate_allow_list(
                tool_version_ids, published_lookup=lookup
            )
            for item in allow_result.get("issues", []):
                issues.append(
                    ValidationIssue(
                        code=item["code"],
                        message=f"Tool allow-list violation: {item.get('tool_version_id')}",
                    )
                )

        skill_ids = parse_uuid_list(av.skill_ids_json)
        for sid in skill_ids:
            skill = self._skills.get(ctx, sid)
            if skill is None:
                issues.append(
                    ValidationIssue(
                        code="SKILL_NOT_FOUND",
                        message=f"Linked skill not found: {sid}",
                    )
                )
            elif skill.status != SkillStatus.PUBLISHED.value:
                issues.append(
                    ValidationIssue(
                        code="SKILL_NOT_PUBLISHED",
                        message=f"Linked skill must be published: {sid}",
                    )
                )

        limits = self._limits_engine.validate(max_steps=av.max_steps, max_tokens=av.max_tokens)
        for item in limits.get("issues", []):
            issues.append(
                ValidationIssue(
                    code=item["code"],
                    message=f"Orchestration limit invalid: {item.get('field')}",
                    field=item.get("field"),
                )
            )

        for policy_id, code, repo in (
            (av.gateway_policy_id, "GATEWAY_POLICY", self._gateway_policies),
            (av.guardrail_policy_id, "GUARDRAIL_POLICY", self._guardrail_policies),
            (av.moderation_policy_id, "MODERATION_POLICY", self._moderation_policies),
            (av.rate_limit_policy_id, "RATE_LIMIT_POLICY", self._rate_limit_policies),
        ):
            if not policy_id:
                continue
            policy = repo.get(ctx, policy_id)
            if policy is None:
                issues.append(
                    ValidationIssue(
                        code=f"{code}_NOT_FOUND",
                        message=f"Linked {code.lower()} not found",
                    )
                )
            elif policy.status != PolicyStatus.PUBLISHED.value:
                issues.append(
                    ValidationIssue(
                        code=f"{code}_NOT_PUBLISHED",
                        message=f"Linked {code.lower()} must be published",
                    )
                )

        if av.knowledge_base_id:
            kb = self._knowledge_bases.get(ctx, av.knowledge_base_id)
            if kb is None:
                issues.append(
                    ValidationIssue(
                        code="KNOWLEDGE_BASE_NOT_FOUND",
                        message="Linked knowledge base not found",
                    )
                )
            elif kb.status != KnowledgeBaseStatus.PUBLISHED.value:
                warnings.append(
                    ValidationIssue(
                        code="KNOWLEDGE_BASE_NOT_PUBLISHED",
                        message="Linked knowledge base is not published",
                        severity="warning",
                    )
                )

        return AgentVersionPublishValidationResult(
            valid=len(issues) == 0,
            agent_version_id=av.id,
            agent_id=av.agent_id,
            issues=issues,
            warnings=warnings,
        )
