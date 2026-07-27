"""AI Provider adapter — invoke via AiGateway (never direct SDK)."""

from uuid import UUID

from modules.ai.adapters.gateway import AiGateway


class AiProviderAdapter:
    def __init__(self) -> None:
        self._gateway = AiGateway()

    def invoke(
        self,
        messages: list[dict],
        *,
        model_ref: UUID | str | None = None,
        credential_ref: UUID | str | None = None,
        guardrail_allowed: bool = True,
        moderation_allowed: bool = True,
        rate_limit_allowed: bool = True,
    ) -> dict:
        return self._gateway.invoke(
            messages,
            model_ref=model_ref,
            credential_ref=credential_ref,
            guardrail_allowed=guardrail_allowed,
            moderation_allowed=moderation_allowed,
            rate_limit_allowed=rate_limit_allowed,
        )
