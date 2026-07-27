"""ai_session ORM per ERD-27 Phase 1."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import SESSION_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in SESSION_STATUS_VALUES)


class AiSession(Base, *AiRowMixin):
    __tablename__ = "ai_session"
    __table_args__ = (
        UniqueConstraint("company_id", "session_code", name="uk_ai_session_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_session_status",
        ),
        Index("ix_ai_session_assistant", "assistant_id"),
        Index("ix_ai_session_configuration", "configuration_id"),
        Index("ix_ai_session_user", "user_id"),
        Index("ix_ai_session_module_entity", "module_code", "entity_id"),
        Index("ix_ai_session_bpm_task", "bpm_task_id"),
        Index("ix_ai_session_expires", "expires_at"),
        Index("ix_ai_session_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="open", index=True)

    assistant_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_assistant.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    # Phase 3 agent version — UUID metadata only; no ai_agent FK
    agent_version_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    configuration_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_configuration.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    # Foundation user UUID — no peer schema FK
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    module_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    bpm_task_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
