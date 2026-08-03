"""Log/trace policy lifecycle — Draft → Published → Retired."""

from datetime import datetime, timezone

from modules.monitoring.domain.enums import LogTracePolicyStatus
from modules.monitoring.domain.exceptions import (
    InvalidLogTracePolicyState,
    PublishedLogTracePolicyImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class LogTracePolicyLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == LogTracePolicyStatus.PUBLISHED.value:
            raise PublishedLogTracePolicyImmutable()
        if row.status == LogTracePolicyStatus.RETIRED.value:
            raise InvalidLogTracePolicyState("Retired log/trace policies are read-only")
        if row.status != LogTracePolicyStatus.DRAFT.value:
            raise InvalidLogTracePolicyState("Only draft log/trace policies are editable")

    def publish(self, row) -> None:
        if row.status != LogTracePolicyStatus.DRAFT.value:
            raise InvalidLogTracePolicyState("Only draft log/trace policies can be published")
        row.status = LogTracePolicyStatus.PUBLISHED.value
        row.published_at = _utcnow()

    def retire(self, row) -> None:
        if row.status == LogTracePolicyStatus.RETIRED.value:
            raise InvalidLogTracePolicyState("Log/trace policy already retired")
        if row.status not in {
            LogTracePolicyStatus.DRAFT.value,
            LogTracePolicyStatus.PUBLISHED.value,
        }:
            raise InvalidLogTracePolicyState("Only draft or published policies can be retired")
        row.status = LogTracePolicyStatus.RETIRED.value
