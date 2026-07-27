"""Routing rule lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.ai.domain.enums import PolicyStatus
from modules.ai.domain.exceptions import (
    InvalidRoutingRuleState,
    PublishedRoutingRuleImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class RoutingRuleEngine:
    def assert_editable(self, row) -> None:
        if row.status == PolicyStatus.PUBLISHED.value:
            raise PublishedRoutingRuleImmutable()
        if row.status == PolicyStatus.RETIRED.value:
            raise InvalidRoutingRuleState("Retired routing rules are read-only")
        if row.status != PolicyStatus.DRAFT.value:
            raise InvalidRoutingRuleState("Only draft routing rules are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != PolicyStatus.DRAFT.value:
            raise InvalidRoutingRuleState("Only draft routing rules can be published")
        row.status = PolicyStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {PolicyStatus.PUBLISHED.value, PolicyStatus.DRAFT.value}:
            raise InvalidRoutingRuleState(
                "Only draft or published routing rules can be retired"
            )
        row.status = PolicyStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
