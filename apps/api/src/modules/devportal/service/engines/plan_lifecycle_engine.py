"""Plan lifecycle engine — Draft → Publish → Retire; published immutable."""

from datetime import datetime, timezone

from modules.devportal.domain.enums import PlanStatus
from modules.devportal.domain.exceptions import InvalidPlanState, PublishedPlanImmutable


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PlanLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == PlanStatus.PUBLISHED.value:
            raise PublishedPlanImmutable()
        if row.status == PlanStatus.RETIRED.value:
            raise InvalidPlanState("Retired plans are read-only")
        if row.status != PlanStatus.DRAFT.value:
            raise InvalidPlanState("Only draft plans are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != PlanStatus.DRAFT.value:
            raise InvalidPlanState("Only draft plans can be published")
        row.status = PlanStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {PlanStatus.PUBLISHED.value, PlanStatus.DRAFT.value}:
            raise InvalidPlanState("Only draft or published plans can be retired")
        row.status = PlanStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
