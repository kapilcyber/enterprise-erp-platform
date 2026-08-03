"""Signal correlation lifecycle — Draft → Active → Retired."""

from modules.monitoring.domain.enums import SignalCorrelationStatus
from modules.monitoring.domain.exceptions import (
    ActiveSignalCorrelationImmutable,
    InvalidSignalCorrelationState,
)


class SignalCorrelationLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == SignalCorrelationStatus.ACTIVE.value:
            raise ActiveSignalCorrelationImmutable()
        if row.status == SignalCorrelationStatus.RETIRED.value:
            raise InvalidSignalCorrelationState("Retired signal correlations are read-only")
        if row.status != SignalCorrelationStatus.DRAFT.value:
            raise InvalidSignalCorrelationState("Only draft signal correlations are editable")

    def activate(self, row) -> None:
        if row.status != SignalCorrelationStatus.DRAFT.value:
            raise InvalidSignalCorrelationState(
                "Only draft signal correlations can be activated"
            )
        row.status = SignalCorrelationStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status == SignalCorrelationStatus.RETIRED.value:
            raise InvalidSignalCorrelationState("Signal correlation already retired")
        if row.status not in {
            SignalCorrelationStatus.DRAFT.value,
            SignalCorrelationStatus.ACTIVE.value,
        }:
            raise InvalidSignalCorrelationState(
                "Only draft or active correlations can be retired"
            )
        row.status = SignalCorrelationStatus.RETIRED.value
