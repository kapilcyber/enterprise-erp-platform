"""Knowledge chunk lifecycle engine — invalidate."""

from modules.ai.domain.enums import KnowledgeChunkStatus
from modules.ai.domain.exceptions import InvalidKnowledgeChunkState


class KnowledgeChunkEngine:
    def invalidate(self, row) -> None:
        if row.status == KnowledgeChunkStatus.INVALIDATED.value:
            raise InvalidKnowledgeChunkState("Knowledge chunk is already invalidated")
        row.status = KnowledgeChunkStatus.INVALIDATED.value
