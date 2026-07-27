"""Skill lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.ai.domain.enums import SkillStatus
from modules.ai.domain.exceptions import InvalidSkillState, PublishedSkillImmutable


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SkillEngine:
    def assert_editable(self, row) -> None:
        if row.status == SkillStatus.PUBLISHED.value:
            raise PublishedSkillImmutable()
        if row.status == SkillStatus.RETIRED.value:
            raise InvalidSkillState("Retired skills are read-only")
        if row.status != SkillStatus.DRAFT.value:
            raise InvalidSkillState("Only draft skills are editable")

    def publish(self, row, *, user_id, publish_reason: str | None = None) -> None:
        if row.status != SkillStatus.DRAFT.value:
            raise InvalidSkillState("Only draft skills can be published")
        row.status = SkillStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id
        if publish_reason is not None:
            row.publish_reason = publish_reason

    def retire(self, row, *, user_id, retire_reason: str | None = None) -> None:
        if row.status not in {SkillStatus.PUBLISHED.value, SkillStatus.DRAFT.value}:
            raise InvalidSkillState("Only draft or published skills can be retired")
        row.status = SkillStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
        if retire_reason is not None:
            row.retire_reason = retire_reason
