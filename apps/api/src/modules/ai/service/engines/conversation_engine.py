"""Conversation lifecycle engine — archive / purge."""

from modules.ai.domain.enums import ConversationStatus
from modules.ai.domain.exceptions import InvalidConversationState


class ConversationEngine:
    def archive(self, row) -> None:
        if row.status != ConversationStatus.ACTIVE.value:
            raise InvalidConversationState("Only active conversations can be archived")
        row.status = ConversationStatus.ARCHIVED.value

    def purge(self, row) -> None:
        if row.status == ConversationStatus.PURGED.value:
            raise InvalidConversationState("Conversation already purged")
        row.status = ConversationStatus.PURGED.value
