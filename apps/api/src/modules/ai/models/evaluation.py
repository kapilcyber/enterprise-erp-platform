"""ai_evaluation ORM per ERD-27 Phase 4 — evaluation run metadata (+ merged results)."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import EVALUATION_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in EVALUATION_STATUS_VALUES)


class AiEvaluation(Base, *AiRowMixin):
    __tablename__ = "ai_evaluation"
    __table_args__ = (
        UniqueConstraint("company_id", "evaluation_code", name="uk_ai_evaluation_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_evaluation_status",
        ),
        Index("ix_ai_evaluation_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_evaluation_prompt_version", "prompt_version_id"),
        Index("ix_ai_evaluation_knowledge_base", "knowledge_base_id"),
        Index("ix_ai_evaluation_guardrail_policy", "guardrail_policy_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    evaluation_code: Mapped[str] = mapped_column(String(50), nullable=False)
    evaluation_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    evaluation_kind: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="queued", index=True)
    dataset_ref_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_summary_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    metrics_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    prompt_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_prompt_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    knowledge_base_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_knowledge_base.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    guardrail_policy_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_guardrail_policy.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    agent_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_agent_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    queued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
