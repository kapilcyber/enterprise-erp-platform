"""API product version lifecycle — Draft → Published → Retired; published immutable."""

from datetime import datetime, timezone

from modules.devportal.domain.enums import ApiProductVersionStatus
from modules.devportal.domain.exceptions import (
    InvalidApiProductVersionState,
    PublishedApiProductVersionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ProductVersionLifecycleEngine:
    def assert_editable(self, row) -> None:
        if row.status == ApiProductVersionStatus.PUBLISHED.value:
            raise PublishedApiProductVersionImmutable()
        if row.status == ApiProductVersionStatus.RETIRED.value:
            raise InvalidApiProductVersionState("Retired product versions are read-only")
        if row.status != ApiProductVersionStatus.DRAFT.value:
            raise InvalidApiProductVersionState("Only draft product versions are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != ApiProductVersionStatus.DRAFT.value:
            raise InvalidApiProductVersionState("Only draft product versions can be published")
        row.status = ApiProductVersionStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {
            ApiProductVersionStatus.PUBLISHED.value,
            ApiProductVersionStatus.DRAFT.value,
        }:
            raise InvalidApiProductVersionState("Only draft or published versions can be retired")
        row.status = ApiProductVersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
