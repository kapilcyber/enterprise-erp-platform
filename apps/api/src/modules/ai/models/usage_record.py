"""ai_usage_record ORM per ERD-27 Phase 1 — append-oriented operational telemetry."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.models.mixins import AiRowMixin


class AiUsageRecord(Base, *AiRowMixin):
    __tablename__ = "ai_usage_record"
    __table_args__ = (
        UniqueConstraint("company_id", "usage_code", name="uk_ai_usage_record_code"),
        CheckConstraint(
            "input_tokens >= 0",
            name="ck_ai_usage_record_input_tokens",
        ),
        CheckConstraint(
            "output_tokens >= 0",
            name="ck_ai_usage_record_output_tokens",
        ),
        CheckConstraint(
            "total_tokens >= 0",
            name="ck_ai_usage_record_total_tokens",
        ),
        Index("ix_ai_usage_record_session", "session_id"),
        Index("ix_ai_usage_record_model", "model_id"),
        Index("ix_ai_usage_record_recorded", "recorded_at"),
        Index("ix_ai_usage_record_tenant_co", "tenant_id", "company_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    usage_code: Mapped[str] = mapped_column(String(50), nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unit_label: Mapped[str | None] = mapped_column(String(50), nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_session.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    model_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_model.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
