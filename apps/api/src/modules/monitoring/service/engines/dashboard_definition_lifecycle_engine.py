"""Dashboard definition lifecycle — Draft → Published → Retired; published immutable."""

from datetime import datetime, timezone

from modules.monitoring.domain.enums import DashboardDefinitionStatus
from modules.monitoring.domain.exceptions import (
    InvalidDashboardDefinitionState,
    PublishedDashboardDefinitionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DashboardDefinitionLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == DashboardDefinitionStatus.PUBLISHED.value:
            raise PublishedDashboardDefinitionImmutable()
        if row.status == DashboardDefinitionStatus.RETIRED.value:
            raise InvalidDashboardDefinitionState("Retired dashboard definitions are read-only")
        if row.status != DashboardDefinitionStatus.DRAFT.value:
            raise InvalidDashboardDefinitionState("Only draft dashboard definitions are editable")

    def publish(self, row) -> None:
        if row.status != DashboardDefinitionStatus.DRAFT.value:
            raise InvalidDashboardDefinitionState(
                "Only draft dashboard definitions can be published"
            )
        row.status = DashboardDefinitionStatus.PUBLISHED.value
        row.published_at = _utcnow()

    def retire(self, row) -> None:
        if row.status == DashboardDefinitionStatus.RETIRED.value:
            raise InvalidDashboardDefinitionState("Dashboard definition already retired")
        if row.status not in {
            DashboardDefinitionStatus.DRAFT.value,
            DashboardDefinitionStatus.PUBLISHED.value,
        }:
            raise InvalidDashboardDefinitionState(
                "Only draft or published dashboards can be retired"
            )
        row.status = DashboardDefinitionStatus.RETIRED.value
