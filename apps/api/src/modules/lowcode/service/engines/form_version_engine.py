"""FormVersion lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.lowcode.domain.enums import VersionStatus
from modules.lowcode.domain.exceptions import (
    InvalidVersionState,
    PublishedVersionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class FormVersionEngine:
    def assert_editable(self, row) -> None:
        if row.status == VersionStatus.PUBLISHED.value:
            raise PublishedVersionImmutable()
        if row.status == VersionStatus.RETIRED.value:
            raise InvalidVersionState("Retired versions are read-only")
        if row.status != VersionStatus.DRAFT.value:
            raise InvalidVersionState("Only draft versions are editable")

    def assert_executable(self, row) -> None:
        from modules.lowcode.domain.exceptions import DraftVersionNotExecutable

        if row.status != VersionStatus.PUBLISHED.value:
            raise DraftVersionNotExecutable(
                f"Runtime requires Published version; current status is '{row.status}'"
            )

    def publish(self, row, *, user_id) -> None:
        if row.status != VersionStatus.DRAFT.value:
            raise InvalidVersionState("Only draft versions can be published")
        row.status = VersionStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {VersionStatus.PUBLISHED.value, VersionStatus.DRAFT.value}:
            raise InvalidVersionState("Only draft or published versions can be retired")
        row.status = VersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id

    def retire_published(self, row, *, user_id) -> None:
        if row.status != VersionStatus.PUBLISHED.value:
            raise InvalidVersionState("Expected a published version to retire")
        row.status = VersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
