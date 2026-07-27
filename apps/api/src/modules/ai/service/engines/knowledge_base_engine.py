"""Knowledge base lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.ai.domain.enums import KnowledgeBaseStatus
from modules.ai.domain.exceptions import InvalidKnowledgeBaseState, PublishedKnowledgeBaseImmutable


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class KnowledgeBaseEngine:
    def assert_editable(self, row) -> None:
        if row.status == KnowledgeBaseStatus.PUBLISHED.value:
            raise PublishedKnowledgeBaseImmutable()
        if row.status == KnowledgeBaseStatus.RETIRED.value:
            raise InvalidKnowledgeBaseState("Retired knowledge bases are read-only")
        if row.status != KnowledgeBaseStatus.DRAFT.value:
            raise InvalidKnowledgeBaseState("Only draft knowledge bases are editable")

    def publish(self, row, *, user_id, publish_reason: str | None = None) -> None:
        if row.status != KnowledgeBaseStatus.DRAFT.value:
            raise InvalidKnowledgeBaseState("Only draft knowledge bases can be published")
        row.status = KnowledgeBaseStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id
        if publish_reason is not None:
            row.publish_reason = publish_reason

    def retire(self, row, *, user_id, retire_reason: str | None = None) -> None:
        if row.status not in {
            KnowledgeBaseStatus.PUBLISHED.value,
            KnowledgeBaseStatus.DRAFT.value,
        }:
            raise InvalidKnowledgeBaseState(
                "Only draft or published knowledge bases can be retired"
            )
        row.status = KnowledgeBaseStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
        if retire_reason is not None:
            row.retire_reason = retire_reason
