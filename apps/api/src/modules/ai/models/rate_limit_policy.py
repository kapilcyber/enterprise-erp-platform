"""ai_rate_limit_policy ORM per ERD-27 Phase 1."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import POLICY_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in POLICY_STATUS_VALUES)


class AiRateLimitPolicy(Base, *AiRowMixin):
    __tablename__ = "ai_rate_limit_policy"
    __table_args__ = (
        UniqueConstraint("company_id", "policy_code", name="uk_ai_rate_limit_policy_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_rate_limit_policy_status",
        ),
        Index("ix_ai_rate_limit_policy_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_rate_limit_policy_name_search", "company_id", "policy_name"),
        Index("ix_ai_rate_limit_policy_code_search", "company_id", "policy_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    policy_code: Mapped[str] = mapped_column(String(50), nullable=False)
    policy_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    policy_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
