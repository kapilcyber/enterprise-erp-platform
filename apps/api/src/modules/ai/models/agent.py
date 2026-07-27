"""ai_agent ORM per ERD-27 Phase 3."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import AGENT_STATUS_VALUES, RISK_CLASS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in AGENT_STATUS_VALUES)
_RISK = ",".join(f"'{t}'" for t in RISK_CLASS_VALUES)


class AiAgent(Base, *AiRowMixin):
    __tablename__ = "ai_agent"
    __table_args__ = (
        UniqueConstraint("company_id", "agent_code", name="uk_ai_agent_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_agent_status",
        ),
        CheckConstraint(
            f"risk_class IS NULL OR risk_class IN ({_RISK})",
            name="ck_ai_agent_risk_class",
        ),
        Index("ix_ai_agent_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_agent_name_search", "company_id", "agent_name"),
        Index("ix_ai_agent_code_search", "company_id", "agent_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    agent_code: Mapped[str] = mapped_column(String(50), nullable=False)
    agent_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_class: Mapped[str | None] = mapped_column(String(30), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    owner_role_ref: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
