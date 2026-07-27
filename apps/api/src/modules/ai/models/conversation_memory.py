"""ai_conversation_memory ORM per ERD-27 Phase 1 — metadata / control-plane only.

No memory runtime, RAG, or semantic retrieval in Phase 1.
"""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import MEMORY_KIND_VALUES, MEMORY_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_KINDS = ",".join(f"'{t}'" for t in MEMORY_KIND_VALUES)
_STATUSES = ",".join(f"'{t}'" for t in MEMORY_STATUS_VALUES)


class AiConversationMemory(Base, *AiRowMixin):
    __tablename__ = "ai_conversation_memory"
    __table_args__ = (
        UniqueConstraint("company_id", "memory_code", name="uk_ai_conversation_memory_code"),
        CheckConstraint(
            f"memory_kind IN ({_KINDS})",
            name="ck_ai_conversation_memory_kind",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_conversation_memory_status",
        ),
        Index("ix_ai_conversation_memory_conversation", "conversation_id"),
        Index("ix_ai_conversation_memory_expires", "expires_at"),
        Index("ix_ai_conversation_memory_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    memory_code: Mapped[str] = mapped_column(String(50), nullable=False)
    memory_kind: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    conversation_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_conversation.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
