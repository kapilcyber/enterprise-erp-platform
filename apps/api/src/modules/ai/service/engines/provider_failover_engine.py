"""Provider failover engine — degraded-mode stub returning provider/model ids."""

from uuid import UUID


class ProviderFailoverEngine:
    def resolve_fallback(
        self,
        rules: list,
        *,
        primary_provider_id: UUID | None = None,
        primary_model_id: UUID | None = None,
    ) -> dict:
        """Return provider/model ids for degraded mode (stub — no live health checks)."""
        if rules:
            rule = sorted(rules, key=lambda r: (r.priority, r.rule_code))[0]
            return {
                "provider_id": rule.provider_id,
                "model_id": rule.model_id,
                "degraded": True,
            }
        return {
            "provider_id": primary_provider_id,
            "model_id": primary_model_id,
            "degraded": primary_provider_id is None,
        }
