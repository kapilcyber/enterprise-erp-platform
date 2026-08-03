"""Observability policy version lifecycle — Draft/In-review → Published → Retired."""

from datetime import datetime, timezone

from modules.monitoring.domain.enums import ObservabilityPolicyVersionStatus
from modules.monitoring.domain.exceptions import (
    InvalidObservabilityPolicyVersionState,
    PublishedObservabilityPolicyVersionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PolicyVersionLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == ObservabilityPolicyVersionStatus.PUBLISHED.value:
            raise PublishedObservabilityPolicyVersionImmutable()
        if row.status == ObservabilityPolicyVersionStatus.RETIRED.value:
            raise InvalidObservabilityPolicyVersionState(
                "Retired observability policy versions are read-only"
            )
        if row.status not in {
            ObservabilityPolicyVersionStatus.DRAFT.value,
            ObservabilityPolicyVersionStatus.IN_REVIEW.value,
        }:
            raise InvalidObservabilityPolicyVersionState(
                "Only draft or in_review policy versions are editable"
            )

    def publish(self, row) -> None:
        if row.status not in {
            ObservabilityPolicyVersionStatus.DRAFT.value,
            ObservabilityPolicyVersionStatus.IN_REVIEW.value,
        }:
            raise InvalidObservabilityPolicyVersionState(
                "Only draft or in_review policy versions can be published"
            )
        row.status = ObservabilityPolicyVersionStatus.PUBLISHED.value
        row.published_at = _utcnow()

    def retire(self, row) -> None:
        if row.status == ObservabilityPolicyVersionStatus.RETIRED.value:
            raise InvalidObservabilityPolicyVersionState("Policy version already retired")
        row.status = ObservabilityPolicyVersionStatus.RETIRED.value
        row.retired_at = _utcnow()
