"""ai_conversation ORM per ERD-27 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import CONVERSATION_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in CONVERSATION_STATUS_VALUES)


class AiConversation(Base, *AiRowMixin):
    __tablename__ = "ai_conversation"
    __table_args__ = (
        UniqueConstraint("company_id", "conversation_code", name="uk_ai_conversation_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_conversation_status",
        ),
        Index("ix_ai_conversation_session", "session_id"),
        Index("ix_ai_conversation_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)

    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_session.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
