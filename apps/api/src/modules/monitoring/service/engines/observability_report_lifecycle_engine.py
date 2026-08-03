"""Observability report lifecycle — Draft → Active → Archived."""

from modules.monitoring.domain.enums import ObservabilityReportStatus
from modules.monitoring.domain.exceptions import (
    ActiveObservabilityReportImmutable,
    InvalidObservabilityReportState,
)


class ObservabilityReportLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == ObservabilityReportStatus.ACTIVE.value:
            raise ActiveObservabilityReportImmutable()
        if row.status == ObservabilityReportStatus.ARCHIVED.value:
            raise InvalidObservabilityReportState("Archived observability reports are read-only")
        if row.status != ObservabilityReportStatus.DRAFT.value:
            raise InvalidObservabilityReportState("Only draft observability reports are editable")

    def activate(self, row) -> None:
        if row.status != ObservabilityReportStatus.DRAFT.value:
            raise InvalidObservabilityReportState(
                "Only draft observability reports can be activated"
            )
        row.status = ObservabilityReportStatus.ACTIVE.value

    def mark_archived(self, row) -> None:
        if row.status == ObservabilityReportStatus.ARCHIVED.value:
            raise InvalidObservabilityReportState("Observability report already archived")
        if row.status not in {
            ObservabilityReportStatus.DRAFT.value,
            ObservabilityReportStatus.ACTIVE.value,
        }:
            raise InvalidObservabilityReportState(
                "Only draft or active reports can be marked archived"
            )
        row.status = ObservabilityReportStatus.ARCHIVED.value
