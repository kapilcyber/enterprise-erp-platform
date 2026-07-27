"""Guardrail / moderation evaluation stub — fail-closed when policy_json missing."""

import json


class GuardrailModerationEngine:
    def evaluate_guardrail(self, policy_json: str | None, *, protected: bool = True) -> bool:
        """Return True if allowed. Fail-closed for protected workloads when policy missing."""
        if not policy_json or not str(policy_json).strip():
            return not protected
        try:
            data = json.loads(policy_json)
        except json.JSONDecodeError:
            return False
        return bool(data.get("enabled", True))

    def evaluate_moderation(self, policy_json: str | None, *, protected: bool = True) -> bool:
        if not policy_json or not str(policy_json).strip():
            return not protected
        try:
            data = json.loads(policy_json)
        except json.JSONDecodeError:
            return False
        return bool(data.get("enabled", True))
