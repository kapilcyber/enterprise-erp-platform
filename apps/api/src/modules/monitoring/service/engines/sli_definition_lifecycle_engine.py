"""SLI definition lifecycle — Draft → Published → Retired; published immutable."""

from datetime import datetime, timezone

from modules.monitoring.domain.enums import SliDefinitionStatus
from modules.monitoring.domain.exceptions import (
    InvalidSliDefinitionState,
    PublishedSliDefinitionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SliDefinitionLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == SliDefinitionStatus.PUBLISHED.value:
            raise PublishedSliDefinitionImmutable()
        if row.status == SliDefinitionStatus.RETIRED.value:
            raise InvalidSliDefinitionState("Retired SLI definitions are read-only")
        if row.status != SliDefinitionStatus.DRAFT.value:
            raise InvalidSliDefinitionState("Only draft SLI definitions are editable")

    def publish(self, row) -> None:
        if row.status != SliDefinitionStatus.DRAFT.value:
            raise InvalidSliDefinitionState("Only draft SLI definitions can be published")
        row.status = SliDefinitionStatus.PUBLISHED.value
        row.published_at = _utcnow()

    def retire(self, row) -> None:
        if row.status == SliDefinitionStatus.RETIRED.value:
            raise InvalidSliDefinitionState("SLI definition already retired")
        if row.status not in {
            SliDefinitionStatus.DRAFT.value,
            SliDefinitionStatus.PUBLISHED.value,
        }:
            raise InvalidSliDefinitionState("Only draft or published SLIs can be retired")
        row.status = SliDefinitionStatus.RETIRED.value
