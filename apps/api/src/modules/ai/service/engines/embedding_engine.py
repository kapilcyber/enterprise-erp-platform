"""Embedding lifecycle engine — mark rebuilt / invalidate (metadata only)."""

from modules.ai.domain.enums import EmbeddingStatus
from modules.ai.domain.exceptions import InvalidEmbeddingState


class EmbeddingEngine:
    def mark_rebuilt(self, row) -> None:
        if row.status == EmbeddingStatus.INVALIDATED.value:
            raise InvalidEmbeddingState("Invalidated embeddings cannot be rebuilt")
        row.status = EmbeddingStatus.REBUILT.value

    def invalidate(self, row) -> None:
        if row.status == EmbeddingStatus.INVALIDATED.value:
            raise InvalidEmbeddingState("Embedding is already invalidated")
        row.status = EmbeddingStatus.INVALIDATED.value
