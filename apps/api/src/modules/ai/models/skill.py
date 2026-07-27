"""ai_skill ORM per ERD-27 Phase 3."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import SKILL_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in SKILL_STATUS_VALUES)


class AiSkill(Base, *AiRowMixin):
    __tablename__ = "ai_skill"
    __table_args__ = (
        UniqueConstraint("company_id", "skill_code", name="uk_ai_skill_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_skill_status",
        ),
        Index("ix_ai_skill_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_skill_name_search", "company_id", "skill_name"),
        Index("ix_ai_skill_code_search", "company_id", "skill_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    skill_code: Mapped[str] = mapped_column(String(50), nullable=False)
    skill_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    tool_version_ids_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")

    prompt_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_prompt_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    publish_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
