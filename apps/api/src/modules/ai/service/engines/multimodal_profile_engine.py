"""Multimodal profile lifecycle engine — draft / publish / retire."""

from datetime import datetime, timezone

from modules.ai.domain.enums import MultimodalProfileStatus
from modules.ai.domain.exceptions import (
    InvalidMultimodalProfileState,
    PublishedMultimodalProfileImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class MultimodalProfileEngine:
    def assert_editable(self, row) -> None:
        if row.status == MultimodalProfileStatus.PUBLISHED.value:
            raise PublishedMultimodalProfileImmutable()
        if row.status == MultimodalProfileStatus.RETIRED.value:
            raise InvalidMultimodalProfileState("Retired multimodal profiles are read-only")
        if row.status != MultimodalProfileStatus.DRAFT.value:
            raise InvalidMultimodalProfileState("Only draft multimodal profiles are editable")

    def publish(self, row, *, user_id, publish_reason: str | None = None) -> None:
        if row.status != MultimodalProfileStatus.DRAFT.value:
            raise InvalidMultimodalProfileState("Only draft multimodal profiles can be published")
        row.status = MultimodalProfileStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id
        if publish_reason is not None:
            row.publish_reason = publish_reason

    def retire(self, row, *, user_id, retire_reason: str | None = None) -> None:
        if row.status not in {
            MultimodalProfileStatus.PUBLISHED.value,
            MultimodalProfileStatus.DRAFT.value,
        }:
            raise InvalidMultimodalProfileState(
                "Only draft or published multimodal profiles can be retired"
            )
        row.status = MultimodalProfileStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
        if retire_reason is not None:
            row.retire_reason = retire_reason
