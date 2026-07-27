"""Provider SDK stub — canned responses only.

Real provider SDKs (OpenAI, Anthropic, Azure, etc.) must live ONLY behind
AiGateway / ProviderSdkStub in adapters/. Services must never import SDKs.
"""

from uuid import UUID


class ProviderSdkStub:
    def invoke(
        self,
        *,
        messages: list[dict],
        model_ref: UUID | str | None = None,
        credential_ref: UUID | str | None = None,
    ) -> dict:
        _ = (model_ref, credential_ref)
        last_user = next(
            (m.get("content", "") for m in reversed(messages) if m.get("role") == "user"),
            "",
        )
        content = f"[stub-response] {last_user[:200]}"
        tokens = max(len(content.split()), 1)
        return {
            "content": content,
            "tokens": {
                "input": sum(len(str(m.get("content", "")).split()) for m in messages),
                "output": tokens,
                "total": tokens + sum(len(str(m.get("content", "")).split()) for m in messages),
            },
        }
