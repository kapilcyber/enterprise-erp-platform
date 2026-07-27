"""Gateway routing engine — select published routing rule by priority (pure)."""

from modules.ai.domain.enums import PolicyStatus


class GatewayRoutingEngine:
    def select_rule(self, rules: list) -> object | None:
        """Return highest-priority published rule, or None."""
        published = [r for r in rules if r.status == PolicyStatus.PUBLISHED.value]
        if not published:
            return None
        return min(published, key=lambda r: (r.priority, r.rule_code))
