"""AgentVersion lifecycle engine — draft / publish / retire / immutability."""

from datetime import datetime, timezone

from modules.ai.domain.enums import AgentVersionStatus
from modules.ai.domain.exceptions import (
    InvalidAgentVersionState,
    PublishedAgentVersionImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AgentVersionEngine:
    def assert_editable(self, row) -> None:
        if row.status == AgentVersionStatus.PUBLISHED.value:
            raise PublishedAgentVersionImmutable()
        if row.status == AgentVersionStatus.RETIRED.value:
            raise InvalidAgentVersionState("Retired agent versions are read-only")
        if row.status != AgentVersionStatus.DRAFT.value:
            raise InvalidAgentVersionState("Only draft agent versions are editable")

    def publish(self, row, *, user_id) -> None:
        if row.status != AgentVersionStatus.DRAFT.value:
            raise InvalidAgentVersionState("Only draft agent versions can be published")
        row.status = AgentVersionStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {
            AgentVersionStatus.PUBLISHED.value,
            AgentVersionStatus.DRAFT.value,
        }:
            raise InvalidAgentVersionState(
                "Only draft or published agent versions can be retired"
            )
        row.status = AgentVersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id

    def retire_published(self, row, *, user_id) -> None:
        if row.status != AgentVersionStatus.PUBLISHED.value:
            raise InvalidAgentVersionState("Expected a published agent version to retire")
        row.status = AgentVersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id
