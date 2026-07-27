"""ai_assistant ORM per ERD-27 Phase 1."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import ASSISTANT_KIND_VALUES, ASSISTANT_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_KINDS = ",".join(f"'{t}'" for t in ASSISTANT_KIND_VALUES)
_STATUSES = ",".join(f"'{t}'" for t in ASSISTANT_STATUS_VALUES)


class AiAssistant(Base, *AiRowMixin):
    __tablename__ = "ai_assistant"
    __table_args__ = (
        UniqueConstraint("company_id", "assistant_code", name="uk_ai_assistant_code"),
        CheckConstraint(
            f"assistant_kind IN ({_KINDS})",
            name="ck_ai_assistant_kind",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_assistant_status",
        ),
        Index("ix_ai_assistant_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_assistant_prompt_version", "prompt_version_id"),
        Index("ix_ai_assistant_configuration", "configuration_id"),
        Index("ix_ai_assistant_gateway_policy", "gateway_policy_id"),
        Index("ix_ai_assistant_name_search", "company_id", "assistant_name"),
        Index("ix_ai_assistant_code_search", "company_id", "assistant_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    assistant_code: Mapped[str] = mapped_column(String(50), nullable=False)
    assistant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    assistant_kind: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    prompt_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_prompt_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    configuration_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_configuration.id", ondelete="RESTRICT"),
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

    # Low-Code UUID refs only — no peer schema FK
    lowcode_form_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    lowcode_page_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
