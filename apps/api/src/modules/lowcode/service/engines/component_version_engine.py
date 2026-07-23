"""ComponentVersion lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.lowcode.domain.enums import VersionStatus
from modules.lowcode.domain.exceptions import (
    InvalidComponentVersionState,
    PublishedComponentVersionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ComponentVersionEngine:
    def assert_editable(self, row) -> None:
        if row.status == VersionStatus.PUBLISHED.value:
            raise PublishedComponentVersionImmutable()
        if row.status == VersionStatus.RETIRED.value:
            raise InvalidComponentVersionState("Retired component versions are read-only")
        if row.status != VersionStatus.DRAFT.value:
            raise InvalidComponentVersionState("Only draft component versions are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != VersionStatus.DRAFT.value:
            raise InvalidComponentVersionState("Only draft versions can be published")
        row.status = VersionStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {VersionStatus.PUBLISHED.value, VersionStatus.DRAFT.value}:
            raise InvalidComponentVersionState(
                "Only draft or published versions can be retired"
            )
        row.status = VersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id

    def retire_published(self, row, *, user_id) -> None:
        if row.status != VersionStatus.PUBLISHED.value:
            raise InvalidComponentVersionState("Expected a published version to retire")
        row.status = VersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
