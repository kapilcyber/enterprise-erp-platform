"""SLO definition lifecycle — Draft → Published → Retired; published immutable."""

from datetime import datetime, timezone

from modules.monitoring.domain.enums import SloDefinitionStatus
from modules.monitoring.domain.exceptions import (
    InvalidSloDefinitionState,
    PublishedSloDefinitionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SloDefinitionLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == SloDefinitionStatus.PUBLISHED.value:
            raise PublishedSloDefinitionImmutable()
        if row.status == SloDefinitionStatus.RETIRED.value:
            raise InvalidSloDefinitionState("Retired SLO definitions are read-only")
        if row.status != SloDefinitionStatus.DRAFT.value:
            raise InvalidSloDefinitionState("Only draft SLO definitions are editable")

    def publish(self, row) -> None:
        if row.status != SloDefinitionStatus.DRAFT.value:
            raise InvalidSloDefinitionState("Only draft SLO definitions can be published")
        row.status = SloDefinitionStatus.PUBLISHED.value
        row.published_at = _utcnow()

    def retire(self, row) -> None:
        if row.status == SloDefinitionStatus.RETIRED.value:
            raise InvalidSloDefinitionState("SLO definition already retired")
        if row.status not in {
            SloDefinitionStatus.DRAFT.value,
            SloDefinitionStatus.PUBLISHED.value,
        }:
            raise InvalidSloDefinitionState("Only draft or published SLOs can be retired")
        row.status = SloDefinitionStatus.RETIRED.value
