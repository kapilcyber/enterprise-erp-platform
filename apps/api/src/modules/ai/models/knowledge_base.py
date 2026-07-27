"""ai_knowledge_base ORM per ERD-27 Phase 2."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import KNOWLEDGE_BASE_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in KNOWLEDGE_BASE_STATUS_VALUES)


class AiKnowledgeBase(Base, *AiRowMixin):
    __tablename__ = "ai_knowledge_base"
    __table_args__ = (
        UniqueConstraint("company_id", "knowledge_base_code", name="uk_ai_knowledge_base_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_knowledge_base_status",
        ),
        Index("ix_ai_knowledge_base_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_knowledge_base_name_search", "company_id", "knowledge_base_name"),
        Index("ix_ai_knowledge_base_code_search", "company_id", "knowledge_base_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    knowledge_base_code: Mapped[str] = mapped_column(String(50), nullable=False)
    knowledge_base_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    classification: Mapped[str | None] = mapped_column(String(100), nullable=True)
    retention_policy_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    access_policy_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    publish_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
