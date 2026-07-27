"""ai_conversation_message ORM per ERD-27 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import MESSAGE_ROLE_VALUES
from modules.ai.models.mixins import AiRowMixin

_ROLES = ",".join(f"'{t}'" for t in MESSAGE_ROLE_VALUES)


class AiConversationMessage(Base, *AiRowMixin):
    __tablename__ = "ai_conversation_message"
    __table_args__ = (
        UniqueConstraint(
            "conversation_id", "sequence_no", name="uk_ai_conversation_message_sequence"
        ),
        CheckConstraint(
            f"message_role IN ({_ROLES})",
            name="ck_ai_conversation_message_role",
        ),
        CheckConstraint(
            "sequence_no >= 0",
            name="ck_ai_conversation_message_sequence_no",
        ),
        Index("ix_ai_conversation_message_conversation", "conversation_id"),
        Index("ix_ai_conversation_message_prompt_version", "prompt_version_id"),
        Index("ix_ai_conversation_message_tenant_co", "tenant_id", "company_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    message_role: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    sequence_no: Mapped[int] = mapped_column(Integer, nullable=False)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    conversation_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_conversation.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    prompt_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_prompt_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    # Phase 3 tool version — UUID metadata only; no ai_tool FK
    tool_version_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
