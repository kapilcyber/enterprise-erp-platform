"""Guardrail policy lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.ai.domain.enums import PolicyStatus
from modules.ai.domain.exceptions import (
    InvalidGuardrailPolicyState,
    PublishedGuardrailPolicyImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class GuardrailPolicyEngine:
    def assert_editable(self, row) -> None:
        if row.status == PolicyStatus.PUBLISHED.value:
            raise PublishedGuardrailPolicyImmutable()
        if row.status == PolicyStatus.RETIRED.value:
            raise InvalidGuardrailPolicyState("Retired guardrail policies are read-only")
        if row.status != PolicyStatus.DRAFT.value:
            raise InvalidGuardrailPolicyState("Only draft guardrail policies are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != PolicyStatus.DRAFT.value:
            raise InvalidGuardrailPolicyState("Only draft guardrail policies can be published")
        row.status = PolicyStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {PolicyStatus.PUBLISHED.value, PolicyStatus.DRAFT.value}:
            raise InvalidGuardrailPolicyState(
                "Only draft or published guardrail policies can be retired"
            )
        row.status = PolicyStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
