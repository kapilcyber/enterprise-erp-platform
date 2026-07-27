"""Agent orchestration limits engine — metadata validation stub (no execution)."""

from modules.ai.domain.exceptions import InvalidAgentVersionState


class AgentOrchestrationLimitsEngine:
    _MAX_STEPS_CEILING = 100
    _MAX_TOKENS_CEILING = 1_000_000

    def validate(self, *, max_steps: int | None, max_tokens: int | None) -> dict:
        issues: list[dict] = []
        if max_steps is not None:
            if max_steps < 1:
                issues.append({"code": "MAX_STEPS_TOO_LOW", "field": "max_steps"})
            elif max_steps > self._MAX_STEPS_CEILING:
                issues.append({"code": "MAX_STEPS_EXCEEDS_CEILING", "field": "max_steps"})
        if max_tokens is not None:
            if max_tokens < 1:
                issues.append({"code": "MAX_TOKENS_TOO_LOW", "field": "max_tokens"})
            elif max_tokens > self._MAX_TOKENS_CEILING:
                issues.append({"code": "MAX_TOKENS_EXCEEDS_CEILING", "field": "max_tokens"})
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "limits_mode": "metadata_stub",
        }

    def assert_valid(self, *, max_steps: int | None, max_tokens: int | None) -> None:
        result = self.validate(max_steps=max_steps, max_tokens=max_tokens)
        if not result["valid"]:
            codes = [i["code"] for i in result["issues"]]
            raise InvalidAgentVersionState(
                f"Orchestration limits validation failed: {codes}"
            )
