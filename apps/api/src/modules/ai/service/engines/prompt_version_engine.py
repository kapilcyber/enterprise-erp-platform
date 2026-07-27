"""PromptVersion lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.ai.domain.enums import PromptVersionStatus
from modules.ai.domain.exceptions import (
    InvalidPromptVersionState,
    PublishedPromptVersionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PromptVersionEngine:
    def assert_editable(self, row) -> None:
        if row.status == PromptVersionStatus.PUBLISHED.value:
            raise PublishedPromptVersionImmutable()
        if row.status == PromptVersionStatus.RETIRED.value:
            raise InvalidPromptVersionState("Retired prompt versions are read-only")
        if row.status != PromptVersionStatus.DRAFT.value:
            raise InvalidPromptVersionState("Only draft prompt versions are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != PromptVersionStatus.DRAFT.value:
            raise InvalidPromptVersionState("Only draft prompt versions can be published")
        row.status = PromptVersionStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {
            PromptVersionStatus.PUBLISHED.value,
            PromptVersionStatus.DRAFT.value,
        }:
            raise InvalidPromptVersionState(
                "Only draft or published prompt versions can be retired"
            )
        row.status = PromptVersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id

    def retire_published(self, row, *, user_id) -> None:
        if row.status != PromptVersionStatus.PUBLISHED.value:
            raise InvalidPromptVersionState("Expected a published prompt version to retire")
        row.status = PromptVersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
