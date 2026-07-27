"""Cache eligibility engine — never bypass guardrails when required."""


class CacheEligibilityEngine:
    def is_eligible(
        self,
        *,
        guardrails_required: bool,
        moderation_required: bool = False,
    ) -> bool:
        """Return False when guardrails (or moderation) must be enforced."""
        return not (guardrails_required or moderation_required)
