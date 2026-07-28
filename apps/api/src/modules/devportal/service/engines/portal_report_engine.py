"""Portal report lifecycle — metadata only; no Analytics warehouse / BI engine."""

from datetime import datetime, timezone
from uuid import UUID

from modules.devportal.domain.enums import (
    PORTAL_REPORT_TYPE_VALUES,
    PortalReportStatus,
)
from modules.devportal.domain.exceptions import (
    AnalyticsWarehouseForbidden,
    InvalidPortalReportState,
    PortalReportProjectionStale,
    PortalReportTypeError,
)


class PortalReportEngine:
    def assert_report_type(self, report_type: str) -> None:
        if report_type not in PORTAL_REPORT_TYPE_VALUES:
            raise PortalReportTypeError(
                f"report_type must be one of {PORTAL_REPORT_TYPE_VALUES}"
            )

    def assert_editable(self, row) -> None:
        if row.status == PortalReportStatus.FINALIZED.value:
            raise InvalidPortalReportState("Finalized portal reports are immutable")
        if row.status == PortalReportStatus.RETIRED.value:
            raise InvalidPortalReportState("Retired portal reports are read-only")
        if row.status != PortalReportStatus.DRAFT.value:
            raise InvalidPortalReportState("Only draft portal reports are editable")

    def finalize(self, row, *, user_id: UUID | None) -> None:
        if row.status != PortalReportStatus.DRAFT.value:
            raise InvalidPortalReportState("Only draft portal reports can be finalized")
        row.status = PortalReportStatus.FINALIZED.value
        row.finalized_at = datetime.now(timezone.utc)
        row.finalized_by = user_id

    def retire(self, row, *, user_id: UUID | None) -> None:
        if row.status not in {
            PortalReportStatus.DRAFT.value,
            PortalReportStatus.FINALIZED.value,
        }:
            raise InvalidPortalReportState(
                "Only draft or finalized portal reports can be retired"
            )
        row.status = PortalReportStatus.RETIRED.value
        row.retired_at = datetime.now(timezone.utc)
        row.retired_by = user_id

    def assert_exportable(self, row) -> None:
        if row.status != PortalReportStatus.FINALIZED.value:
            raise InvalidPortalReportState("Only finalized portal reports can be exported")

    def assert_projection_freshness(self, row) -> None:
        """Pure policy — Hub remains metering SoR; snapshot must exist for export."""
        if row.report_type == "hub_usage" and not row.projection_snapshot_json:
            raise PortalReportProjectionStale()

    def assert_metadata_only(self) -> None:
        raise AnalyticsWarehouseForbidden()
