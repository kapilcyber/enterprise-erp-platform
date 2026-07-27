"""AI Gateway — apply policies then delegate to ProviderSdkStub."""

from uuid import UUID

from modules.ai.adapters.provider_sdk_stub import ProviderSdkStub


class AiGateway:
    def __init__(self) -> None:
        self._sdk = ProviderSdkStub()

    def apply_policies(
        self,
        *,
        guardrail_allowed: bool,
        moderation_allowed: bool,
        rate_limit_allowed: bool,
    ) -> None:
        if not guardrail_allowed:
            raise PermissionError("Guardrail policy blocked invocation")
        if not moderation_allowed:
            raise PermissionError("Moderation policy blocked invocation")
        if not rate_limit_allowed:
            raise PermissionError("Rate limit policy blocked invocation")

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
        self.apply_policies(
            guardrail_allowed=guardrail_allowed,
            moderation_allowed=moderation_allowed,
            rate_limit_allowed=rate_limit_allowed,
        )
        return self._sdk.invoke(
            messages=messages,
            model_ref=model_ref,
            credential_ref=credential_ref,
        )
