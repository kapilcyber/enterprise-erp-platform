"""Runtime resolve — published assistant + prompt + routing via engines (no provider SDK)."""

import json
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import AppException, NotFoundException
from modules.ai.repository.assistant_repository import AssistantRepository
from modules.ai.repository.guardrail_policy_repository import GuardrailPolicyRepository
from modules.ai.repository.moderation_policy_repository import ModerationPolicyRepository
from modules.ai.repository.prompt_version_repository import PromptVersionRepository
from modules.ai.repository.rate_limit_policy_repository import RateLimitPolicyRepository
from modules.ai.repository.routing_rule_repository import RoutingRuleRepository
from modules.ai.service.engines import GatewayRoutingEngine, PublishGateEngine
from modules.foundation.domain.value_objects import TenantContext


class RuntimeResolveService:
    def __init__(self, db: Session) -> None:
        self._assistants = AssistantRepository(db)
        self._prompt_versions = PromptVersionRepository(db)
        self._routing_rules = RoutingRuleRepository(db)
        self._guardrail_policies = GuardrailPolicyRepository(db)
        self._moderation_policies = ModerationPolicyRepository(db)
        self._rate_limit_policies = RateLimitPolicyRepository(db)
        self._routing = GatewayRoutingEngine()
        self._gate = PublishGateEngine()

    def resolve(self, ctx: TenantContext, **fields) -> dict:
        assistant_id = fields.get("assistant_id")
        if assistant_id is None:
            raise AppException("assistant_id is required")
        resolved = self.resolve_assistant(ctx, assistant_id)
        assistant = self._assistants.get(ctx, assistant_id)
        return {
            "assistant_id": resolved["assistant_id"],
            "prompt_version_id": resolved["prompt_version_id"],
            "configuration_id": assistant.configuration_id if assistant else None,
            "model_id": resolved.get("model_id"),
            "provider_id": resolved.get("provider_id"),
            "gateway_policy_id": assistant.gateway_policy_id if assistant else None,
            "guardrail_policy_id": resolved.get("guardrail_policy_id"),
            "moderation_policy_id": resolved.get("moderation_policy_id"),
            "rate_limit_policy_id": resolved.get("rate_limit_policy_id"),
            "resolved_json": json.dumps(resolved, default=str),
        }

    def resolve_assistant(self, ctx: TenantContext, assistant_id: UUID) -> dict:
        assistant = self._assistants.get(ctx, assistant_id)
        if assistant is None:
            raise NotFoundException("Assistant not found")
        self._gate.assert_assistant_published(assistant.status)

        prompt_version = self._prompt_versions.get(ctx, assistant.prompt_version_id)
        if prompt_version is None:
            raise NotFoundException("Prompt version not found")
        self._gate.assert_prompt_version_published(prompt_version.status)

        routing_rule = None
        if assistant.gateway_policy_id:
            rules = self._routing_rules.list_by_gateway_policy(
                ctx, assistant.gateway_policy_id
            )
            routing_rule = self._routing.select_rule(rules)

        guardrail_policy = None
        if assistant.guardrail_policy_id:
            guardrail_policy = self._guardrail_policies.get(ctx, assistant.guardrail_policy_id)
            if guardrail_policy:
                self._gate.assert_guardrail_policy_published(guardrail_policy.status)

        moderation_policy = None
        if assistant.moderation_policy_id:
            moderation_policy = self._moderation_policies.get(
                ctx, assistant.moderation_policy_id
            )
            if moderation_policy:
                self._gate.assert_moderation_policy_published(moderation_policy.status)

        rate_limit_policy = None
        if assistant.rate_limit_policy_id:
            rate_limit_policy = self._rate_limit_policies.get(
                ctx, assistant.rate_limit_policy_id
            )
            if rate_limit_policy:
                self._gate.assert_rate_limit_policy_published(rate_limit_policy.status)

        return {
            "assistant_id": assistant.id,
            "assistant_code": assistant.assistant_code,
            "prompt_version_id": prompt_version.id,
            "prompt_content": prompt_version.content_text,
            "routing_rule_id": routing_rule.id if routing_rule else None,
            "provider_id": routing_rule.provider_id if routing_rule else None,
            "model_id": routing_rule.model_id if routing_rule else None,
            "guardrail_policy_id": (
                guardrail_policy.id if guardrail_policy else None
            ),
            "guardrail_policy_json": (
                guardrail_policy.policy_json if guardrail_policy else None
            ),
            "moderation_policy_id": (
                moderation_policy.id if moderation_policy else None
            ),
            "moderation_policy_json": (
                moderation_policy.policy_json if moderation_policy else None
            ),
            "rate_limit_policy_id": (
                rate_limit_policy.id if rate_limit_policy else None
            ),
            "rate_limit_policy_json": (
                rate_limit_policy.policy_json if rate_limit_policy else None
            ),
        }
