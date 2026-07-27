"""Conversation message engine — role / sequence validation (append-only)."""

from modules.ai.domain.enums import MESSAGE_ROLE_VALUES
from modules.ai.domain.exceptions import InvalidConversationMessageState


class ConversationMessageEngine:
    def validate_role(self, message_role: str) -> None:
        if message_role not in MESSAGE_ROLE_VALUES:
            raise InvalidConversationMessageState(f"Invalid message role: {message_role}")

    def validate_sequence(self, expected: int, actual: int) -> None:
        if actual != expected:
            raise InvalidConversationMessageState(
                f"Expected sequence_no {expected}, got {actual}"
            )

    def assert_content_immutable(self, row, *, content_text: str | None = None) -> None:
        """Optional guard: content cannot change after create."""
        if content_text is not None and content_text != row.content_text:
            raise InvalidConversationMessageState(
                "Conversation message content is append-only and cannot be updated"
            )
