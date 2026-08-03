"""Alert rule lifecycle — Draft/In-review → Published → Retired."""

from datetime import datetime, timezone

from modules.monitoring.domain.enums import AlertRuleStatus
from modules.monitoring.domain.exceptions import (
    InvalidAlertRuleState,
    PublishedAlertRuleImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AlertRuleLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == AlertRuleStatus.PUBLISHED.value:
            raise PublishedAlertRuleImmutable()
        if row.status == AlertRuleStatus.RETIRED.value:
            raise InvalidAlertRuleState("Retired alert rules are read-only")
        if row.status not in {
            AlertRuleStatus.DRAFT.value,
            AlertRuleStatus.IN_REVIEW.value,
        }:
            raise InvalidAlertRuleState("Only draft or in_review alert rules are editable")

    def publish(self, row) -> None:
        if row.status not in {
            AlertRuleStatus.DRAFT.value,
            AlertRuleStatus.IN_REVIEW.value,
        }:
            raise InvalidAlertRuleState("Only draft or in_review alert rules can be published")
        row.status = AlertRuleStatus.PUBLISHED.value
        row.published_at = _utcnow()

    def retire(self, row) -> None:
        if row.status == AlertRuleStatus.RETIRED.value:
            raise InvalidAlertRuleState("Alert rule already retired")
        row.status = AlertRuleStatus.RETIRED.value
