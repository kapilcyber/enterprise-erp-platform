"""External platform binding lifecycle — Draft/In-review → Active → Retired."""

from datetime import datetime, timezone

from modules.monitoring.domain.enums import ExternalPlatformBindingStatus
from modules.monitoring.domain.exceptions import (
    ActiveExternalPlatformBindingImmutable,
    InvalidExternalPlatformBindingState,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ExternalPlatformBindingLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == ExternalPlatformBindingStatus.ACTIVE.value:
            raise ActiveExternalPlatformBindingImmutable()
        if row.status == ExternalPlatformBindingStatus.RETIRED.value:
            raise InvalidExternalPlatformBindingState(
                "Retired external platform bindings are read-only"
            )
        if row.status not in {
            ExternalPlatformBindingStatus.DRAFT.value,
            ExternalPlatformBindingStatus.IN_REVIEW.value,
        }:
            raise InvalidExternalPlatformBindingState(
                "Only draft or in_review bindings are editable"
            )

    def activate(self, row) -> None:
        if row.status not in {
            ExternalPlatformBindingStatus.DRAFT.value,
            ExternalPlatformBindingStatus.IN_REVIEW.value,
        }:
            raise InvalidExternalPlatformBindingState(
                "Only draft or in_review bindings can be activated"
            )
        row.status = ExternalPlatformBindingStatus.ACTIVE.value
        row.activated_at = _utcnow()

    def retire(self, row) -> None:
        if row.status == ExternalPlatformBindingStatus.RETIRED.value:
            raise InvalidExternalPlatformBindingState("Binding already retired")
        row.status = ExternalPlatformBindingStatus.RETIRED.value
