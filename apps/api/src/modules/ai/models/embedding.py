"""ai_embedding ORM per ERD-27 Phase 2."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import EMBEDDING_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in EMBEDDING_STATUS_VALUES)


class AiEmbedding(Base, *AiRowMixin):
    __tablename__ = "ai_embedding"
    __table_args__ = (
        UniqueConstraint("company_id", "embedding_code", name="uk_ai_embedding_code"),
        UniqueConstraint(
            "knowledge_chunk_id",
            "model_id",
            name="uk_ai_embedding_chunk_model",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_embedding_status",
        ),
        Index("ix_ai_embedding_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_embedding_chunk", "knowledge_chunk_id"),
        Index("ix_ai_embedding_model", "model_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    knowledge_chunk_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_knowledge_chunk.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    model_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_model.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    embedding_code: Mapped[str] = mapped_column(String(50), nullable=False)
    dimensions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="created", index=True)
    vector_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
