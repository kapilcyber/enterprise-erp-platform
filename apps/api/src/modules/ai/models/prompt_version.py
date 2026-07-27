"""ai_prompt_version ORM per ERD-27 Phase 1."""

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
from modules.ai.domain.enums import PROMPT_VERSION_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in PROMPT_VERSION_STATUS_VALUES)


class AiPromptVersion(Base, *AiRowMixin):
    __tablename__ = "ai_prompt_version"
    __table_args__ = (
        UniqueConstraint(
            "template_id", "version_number", name="uk_ai_prompt_version_number"
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_prompt_version_status",
        ),
        Index("ix_ai_prompt_version_template_status", "template_id", "status"),
        Index("ix_ai_prompt_version_tenant_co", "tenant_id", "company_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    version_code: Mapped[str] = mapped_column(String(50), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    version_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    change_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)

    template_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_prompt_template.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    publish_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    cloned_from_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_prompt_version.id", ondelete="SET NULL"),
        nullable=True,
    )
