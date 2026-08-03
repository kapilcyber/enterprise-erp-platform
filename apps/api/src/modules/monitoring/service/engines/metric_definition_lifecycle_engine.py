"""Metric definition lifecycle — Draft → Published → Retired; published immutable."""

from datetime import datetime, timezone

from modules.monitoring.domain.enums import MetricDefinitionStatus
from modules.monitoring.domain.exceptions import (
    InvalidMetricDefinitionState,
    PublishedMetricDefinitionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class MetricDefinitionLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == MetricDefinitionStatus.PUBLISHED.value:
            raise PublishedMetricDefinitionImmutable()
        if row.status == MetricDefinitionStatus.RETIRED.value:
            raise InvalidMetricDefinitionState("Retired metric definitions are read-only")
        if row.status != MetricDefinitionStatus.DRAFT.value:
            raise InvalidMetricDefinitionState("Only draft metric definitions are editable")

    def publish(self, row) -> None:
        if row.status != MetricDefinitionStatus.DRAFT.value:
            raise InvalidMetricDefinitionState("Only draft metric definitions can be published")
        row.status = MetricDefinitionStatus.PUBLISHED.value
        row.published_at = _utcnow()

    def retire(self, row) -> None:
        if row.status == MetricDefinitionStatus.RETIRED.value:
            raise InvalidMetricDefinitionState("Metric definition already retired")
        if row.status not in {
            MetricDefinitionStatus.DRAFT.value,
            MetricDefinitionStatus.PUBLISHED.value,
        }:
            raise InvalidMetricDefinitionState("Only draft or published metrics can be retired")
        row.status = MetricDefinitionStatus.RETIRED.value
