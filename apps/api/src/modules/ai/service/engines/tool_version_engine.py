"""ToolVersion lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.ai.domain.enums import ToolVersionStatus
from modules.ai.domain.exceptions import InvalidToolVersionState, PublishedToolVersionImmutable


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ToolVersionEngine:
    def assert_editable(self, row) -> None:
        if row.status == ToolVersionStatus.PUBLISHED.value:
            raise PublishedToolVersionImmutable()
        if row.status == ToolVersionStatus.RETIRED.value:
            raise InvalidToolVersionState("Retired tool versions are read-only")
        if row.status != ToolVersionStatus.DRAFT.value:
            raise InvalidToolVersionState("Only draft tool versions are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != ToolVersionStatus.DRAFT.value:
            raise InvalidToolVersionState("Only draft tool versions can be published")
        row.status = ToolVersionStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {
            ToolVersionStatus.PUBLISHED.value,
            ToolVersionStatus.DRAFT.value,
        }:
            raise InvalidToolVersionState(
                "Only draft or published tool versions can be retired"
            )
        row.status = ToolVersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id

    def retire_published(self, row, *, user_id) -> None:
        if row.status != ToolVersionStatus.PUBLISHED.value:
            raise InvalidToolVersionState("Expected a published tool version to retire")
        row.status = ToolVersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
