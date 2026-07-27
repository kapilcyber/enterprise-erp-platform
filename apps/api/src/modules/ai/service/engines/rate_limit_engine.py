"""Rate limit engine — stub allow/deny from policy_json."""

import json


class RateLimitEngine:
    def allow(self, policy_json: str | None, *, key: str | None = None) -> bool:
        if not policy_json or not str(policy_json).strip():
            return True
        try:
            data = json.loads(policy_json)
        except json.JSONDecodeError:
            return False
        if not data.get("enabled", True):
            return True
        deny_keys = data.get("deny_keys") or []
        return not (key and key in deny_keys)
