"""Alert routing policy lifecycle — Draft/In-review → Published → Retired."""

from datetime import datetime, timezone

from modules.monitoring.domain.enums import AlertRoutingPolicyStatus
from modules.monitoring.domain.exceptions import (
    InvalidAlertRoutingPolicyState,
    PublishedAlertRoutingPolicyImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AlertRoutingPolicyLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == AlertRoutingPolicyStatus.PUBLISHED.value:
            raise PublishedAlertRoutingPolicyImmutable()
        if row.status == AlertRoutingPolicyStatus.RETIRED.value:
            raise InvalidAlertRoutingPolicyState(
                "Retired alert routing policies are read-only"
            )
        if row.status not in {
            AlertRoutingPolicyStatus.DRAFT.value,
            AlertRoutingPolicyStatus.IN_REVIEW.value,
        }:
            raise InvalidAlertRoutingPolicyState(
                "Only draft or in_review routing policies are editable"
            )

    def publish(self, row) -> None:
        if row.status not in {
            AlertRoutingPolicyStatus.DRAFT.value,
            AlertRoutingPolicyStatus.IN_REVIEW.value,
        }:
            raise InvalidAlertRoutingPolicyState(
                "Only draft or in_review routing policies can be published"
            )
        row.status = AlertRoutingPolicyStatus.PUBLISHED.value
        row.published_at = _utcnow()

    def retire(self, row) -> None:
        if row.status == AlertRoutingPolicyStatus.RETIRED.value:
            raise InvalidAlertRoutingPolicyState("Alert routing policy already retired")
        row.status = AlertRoutingPolicyStatus.RETIRED.value
