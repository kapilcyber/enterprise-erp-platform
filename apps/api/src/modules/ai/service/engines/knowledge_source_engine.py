"""Knowledge source lifecycle engine — activate / suspend / retire."""

from modules.ai.domain.enums import KnowledgeSourceStatus
from modules.ai.domain.exceptions import InvalidKnowledgeSourceState


class KnowledgeSourceEngine:
    def activate(self, row) -> None:
        if row.status == KnowledgeSourceStatus.ACTIVE.value:
            raise InvalidKnowledgeSourceState("Knowledge source is already active")
        if row.status == KnowledgeSourceStatus.RETIRED.value:
            raise InvalidKnowledgeSourceState("Retired knowledge sources cannot be activated")
        row.status = KnowledgeSourceStatus.ACTIVE.value

    def suspend(self, row) -> None:
        if row.status != KnowledgeSourceStatus.ACTIVE.value:
            raise InvalidKnowledgeSourceState("Only active knowledge sources can be suspended")
        row.status = KnowledgeSourceStatus.SUSPENDED.value

    def retire(self, row) -> None:
        if row.status == KnowledgeSourceStatus.RETIRED.value:
            raise InvalidKnowledgeSourceState("Knowledge source is already retired")
        row.status = KnowledgeSourceStatus.RETIRED.value
