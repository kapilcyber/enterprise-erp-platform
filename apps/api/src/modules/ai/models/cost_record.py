"""ai_cost_record ORM per ERD-27 Phase 1 — append-oriented cost telemetry."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.models.mixins import AiRowMixin


class AiCostRecord(Base, *AiRowMixin):
    __tablename__ = "ai_cost_record"
    __table_args__ = (
        UniqueConstraint("company_id", "cost_code", name="uk_ai_cost_record_code"),
        CheckConstraint(
            "amount >= 0",
            name="ck_ai_cost_record_amount",
        ),
        Index("ix_ai_cost_record_session", "session_id"),
        Index("ix_ai_cost_record_model", "model_id"),
        Index("ix_ai_cost_record_recorded", "recorded_at"),
        Index("ix_ai_cost_record_tenant_co", "tenant_id", "company_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    cost_code: Mapped[str] = mapped_column(String(50), nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

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
