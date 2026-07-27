"""Publish gate helpers — central published-status checks."""

from modules.ai.domain.enums import AssistantStatus, PolicyStatus, PromptVersionStatus
from modules.ai.domain.exceptions import (
    InvalidAssistantState,
    InvalidGatewayPolicyState,
    InvalidGuardrailPolicyState,
    InvalidModerationPolicyState,
    InvalidPromptVersionState,
    InvalidRateLimitPolicyState,
    InvalidRoutingRuleState,
)


class PublishGateEngine:
    @staticmethod
    def is_prompt_version_published(status: str) -> bool:
        return status == PromptVersionStatus.PUBLISHED.value

    @staticmethod
    def is_policy_published(status: str) -> bool:
        return status == PolicyStatus.PUBLISHED.value

    @staticmethod
    def is_assistant_published(status: str) -> bool:
        return status == AssistantStatus.PUBLISHED.value

    @staticmethod
    def assert_prompt_version_published(status: str) -> None:
        if not PublishGateEngine.is_prompt_version_published(status):
            raise InvalidPromptVersionState("Prompt version must be published")

    @staticmethod
    def assert_assistant_published(status: str) -> None:
        if not PublishGateEngine.is_assistant_published(status):
            raise InvalidAssistantState("Assistant must be published")

    @staticmethod
    def assert_gateway_policy_published(status: str) -> None:
        if not PublishGateEngine.is_policy_published(status):
            raise InvalidGatewayPolicyState("Gateway policy must be published")

    @staticmethod
    def assert_routing_rule_published(status: str) -> None:
        if not PublishGateEngine.is_policy_published(status):
            raise InvalidRoutingRuleState("Routing rule must be published")

    @staticmethod
    def assert_guardrail_policy_published(status: str) -> None:
        if not PublishGateEngine.is_policy_published(status):
            raise InvalidGuardrailPolicyState("Guardrail policy must be published")

    @staticmethod
    def assert_moderation_policy_published(status: str) -> None:
        if not PublishGateEngine.is_policy_published(status):
            raise InvalidModerationPolicyState("Moderation policy must be published")

    @staticmethod
    def assert_rate_limit_policy_published(status: str) -> None:
        if not PublishGateEngine.is_policy_published(status):
            raise InvalidRateLimitPolicyState("Rate limit policy must be published")
