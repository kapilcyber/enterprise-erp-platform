"""ai_feedback ORM per ERD-27 Phase 4."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import FEEDBACK_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in FEEDBACK_STATUS_VALUES)


class AiFeedback(Base, *AiRowMixin):
    __tablename__ = "ai_feedback"
    __table_args__ = (
        UniqueConstraint("company_id", "feedback_code", name="uk_ai_feedback_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_feedback_status",
        ),
        Index("ix_ai_feedback_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_feedback_session", "session_id"),
        Index("ix_ai_feedback_conversation", "conversation_id"),
        Index("ix_ai_feedback_message", "message_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    feedback_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="captured", index=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    correction_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    feedback_kind: Mapped[str | None] = mapped_column(String(50), nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    session_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_session.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    conversation_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_conversation.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    message_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_conversation_message.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    # BPM / case UUID ref only — no peer schema FK
    bpm_case_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewed_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
