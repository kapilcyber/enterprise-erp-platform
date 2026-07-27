"""Assistant lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.ai.domain.enums import AssistantStatus
from modules.ai.domain.exceptions import InvalidAssistantState, PublishedAssistantImmutable


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AssistantEngine:
    def assert_editable(self, row) -> None:
        if row.status == AssistantStatus.PUBLISHED.value:
            raise PublishedAssistantImmutable()
        if row.status == AssistantStatus.RETIRED.value:
            raise InvalidAssistantState("Retired assistants are read-only")
        if row.status != AssistantStatus.DRAFT.value:
            raise InvalidAssistantState("Only draft assistants are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != AssistantStatus.DRAFT.value:
            raise InvalidAssistantState("Only draft assistants can be published")
        row.status = AssistantStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {AssistantStatus.PUBLISHED.value, AssistantStatus.DRAFT.value}:
            raise InvalidAssistantState("Only draft or published assistants can be retired")
        row.status = AssistantStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
