"""PageVersion lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.lowcode.domain.enums import VersionStatus
from modules.lowcode.domain.exceptions import (
    InvalidPageVersionState,
    PublishedPageVersionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PageVersionEngine:
    def assert_editable(self, row) -> None:
        if row.status == VersionStatus.PUBLISHED.value:
            raise PublishedPageVersionImmutable()
        if row.status == VersionStatus.RETIRED.value:
            raise InvalidPageVersionState("Retired page versions are read-only")
        if row.status != VersionStatus.DRAFT.value:
            raise InvalidPageVersionState("Only draft page versions are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != VersionStatus.DRAFT.value:
            raise InvalidPageVersionState("Only draft page versions can be published")
        row.status = VersionStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {VersionStatus.PUBLISHED.value, VersionStatus.DRAFT.value}:
            raise InvalidPageVersionState(
                "Only draft or published page versions can be retired"
            )
        row.status = VersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id

    def retire_published(self, row, *, user_id) -> None:
        if row.status != VersionStatus.PUBLISHED.value:
            raise InvalidPageVersionState("Expected a published page version to retire")
        row.status = VersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
