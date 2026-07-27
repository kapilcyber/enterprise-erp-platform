"""ai_agent_version ORM per ERD-27 Phase 3."""

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
from modules.ai.domain.enums import AGENT_VERSION_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in AGENT_VERSION_STATUS_VALUES)


class AiAgentVersion(Base, *AiRowMixin):
    __tablename__ = "ai_agent_version"
    __table_args__ = (
        UniqueConstraint("agent_id", "version_number", name="uk_ai_agent_version_number"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_agent_version_status",
        ),
        Index("ix_ai_agent_version_agent_status", "agent_id", "status"),
        Index("ix_ai_agent_version_tenant_co", "tenant_id", "company_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    version_code: Mapped[str] = mapped_column(String(50), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    version_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    skill_ids_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    tool_version_ids_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    max_steps: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hitl_policy_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    orchestration_limits_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    agent_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_agent.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    prompt_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_prompt_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    knowledge_base_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_knowledge_base.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    gateway_policy_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_gateway_policy.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    guardrail_policy_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_guardrail_policy.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    moderation_policy_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_moderation_policy.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    rate_limit_policy_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_rate_limit_policy.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    # BPM UUID ref only — no peer schema FK
    bpm_definition_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    publish_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    cloned_from_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_agent_version.id", ondelete="SET NULL"),
        nullable=True,
    )
