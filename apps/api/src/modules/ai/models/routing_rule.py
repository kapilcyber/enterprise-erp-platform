"""ai_routing_rule ORM per ERD-27 Phase 1."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
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
from modules.ai.domain.enums import POLICY_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in POLICY_STATUS_VALUES)


class AiRoutingRule(Base, *AiRowMixin):
    __tablename__ = "ai_routing_rule"
    __table_args__ = (
        UniqueConstraint("company_id", "rule_code", name="uk_ai_routing_rule_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_routing_rule_status",
        ),
        CheckConstraint(
            "priority >= 0",
            name="ck_ai_routing_rule_priority",
        ),
        Index("ix_ai_routing_rule_gateway_policy", "gateway_policy_id"),
        Index("ix_ai_routing_rule_provider", "provider_id"),
        Index("ix_ai_routing_rule_model", "model_id"),
        Index("ix_ai_routing_rule_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    rule_code: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    rule_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    gateway_policy_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_gateway_policy.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    provider_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_provider.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    model_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_model.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
