"""Gateway policy lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.ai.domain.enums import PolicyStatus
from modules.ai.domain.exceptions import (
    InvalidGatewayPolicyState,
    PublishedGatewayPolicyImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class GatewayPolicyEngine:
    def assert_editable(self, row) -> None:
        if row.status == PolicyStatus.PUBLISHED.value:
            raise PublishedGatewayPolicyImmutable()
        if row.status == PolicyStatus.RETIRED.value:
            raise InvalidGatewayPolicyState("Retired gateway policies are read-only")
        if row.status != PolicyStatus.DRAFT.value:
            raise InvalidGatewayPolicyState("Only draft gateway policies are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != PolicyStatus.DRAFT.value:
            raise InvalidGatewayPolicyState("Only draft gateway policies can be published")
        row.status = PolicyStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {PolicyStatus.PUBLISHED.value, PolicyStatus.DRAFT.value}:
            raise InvalidGatewayPolicyState(
                "Only draft or published gateway policies can be retired"
            )
        row.status = PolicyStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
