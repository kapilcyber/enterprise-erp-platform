"""ai_knowledge_source ORM per ERD-27 Phase 2."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import KNOWLEDGE_SOURCE_KIND_VALUES, KNOWLEDGE_SOURCE_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_KINDS = ",".join(f"'{t}'" for t in KNOWLEDGE_SOURCE_KIND_VALUES)
_STATUSES = ",".join(f"'{t}'" for t in KNOWLEDGE_SOURCE_STATUS_VALUES)


class AiKnowledgeSource(Base, *AiRowMixin):
    __tablename__ = "ai_knowledge_source"
    __table_args__ = (
        UniqueConstraint("company_id", "source_code", name="uk_ai_knowledge_source_code"),
        CheckConstraint(
            f"source_kind IN ({_KINDS})",
            name="ck_ai_knowledge_source_kind",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_knowledge_source_status",
        ),
        Index("ix_ai_knowledge_source_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_knowledge_source_kb", "knowledge_base_id"),
        Index("ix_ai_knowledge_source_code_search", "company_id", "source_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    knowledge_base_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_knowledge_base.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    source_code: Mapped[str] = mapped_column(String(50), nullable=False)
    source_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_kind: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    # Document SoR UUID ref only — no peer schema FK
    document_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    external_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
