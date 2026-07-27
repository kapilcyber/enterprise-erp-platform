"""Conversation memory engine — expire / purge metadata only (no semantic retrieval)."""

from modules.ai.domain.enums import MemoryStatus
from modules.ai.domain.exceptions import InvalidConversationMemoryState


class ConversationMemoryEngine:
    def expire(self, row) -> None:
        if row.status != MemoryStatus.ACTIVE.value:
            raise InvalidConversationMemoryState("Only active memory records can be expired")
        row.status = MemoryStatus.EXPIRED.value

    def purge(self, row) -> None:
        if row.status == MemoryStatus.PURGED.value:
            raise InvalidConversationMemoryState("Memory record already purged")
        row.status = MemoryStatus.PURGED.value
