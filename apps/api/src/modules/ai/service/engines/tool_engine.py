"""Tool catalog lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.ai.domain.enums import ToolStatus
from modules.ai.domain.exceptions import InvalidToolState, PublishedToolImmutable


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ToolEngine:
    def assert_editable(self, row) -> None:
        if row.status == ToolStatus.PUBLISHED.value:
            raise PublishedToolImmutable()
        if row.status == ToolStatus.RETIRED.value:
            raise InvalidToolState("Retired tools are read-only")
        if row.status != ToolStatus.DRAFT.value:
            raise InvalidToolState("Only draft tools are editable")

    def publish(self, row, *, user_id, publish_reason: str | None = None) -> None:
        if row.status != ToolStatus.DRAFT.value:
            raise InvalidToolState("Only draft tools can be published")
        row.status = ToolStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id
        if publish_reason is not None:
            row.publish_reason = publish_reason

    def retire(self, row, *, user_id, retire_reason: str | None = None) -> None:
        if row.status not in {ToolStatus.PUBLISHED.value, ToolStatus.DRAFT.value}:
            raise InvalidToolState("Only draft or published tools can be retired")
        row.status = ToolStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
        if retire_reason is not None:
            row.retire_reason = retire_reason
