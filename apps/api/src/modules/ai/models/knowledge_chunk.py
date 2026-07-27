"""ai_knowledge_chunk ORM per ERD-27 Phase 2."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import KNOWLEDGE_CHUNK_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in KNOWLEDGE_CHUNK_STATUS_VALUES)


class AiKnowledgeChunk(Base, *AiRowMixin):
    __tablename__ = "ai_knowledge_chunk"
    __table_args__ = (
        UniqueConstraint("company_id", "chunk_code", name="uk_ai_knowledge_chunk_code"),
        UniqueConstraint(
            "knowledge_source_id",
            "sequence_no",
            name="uk_ai_knowledge_chunk_seq",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_knowledge_chunk_status",
        ),
        Index("ix_ai_knowledge_chunk_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_knowledge_chunk_source", "knowledge_source_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    knowledge_source_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_knowledge_source.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    chunk_code: Mapped[str] = mapped_column(String(50), nullable=False)
    sequence_no: Mapped[int] = mapped_column(Integer, nullable=False)
    content_preview: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    token_estimate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="created", index=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
