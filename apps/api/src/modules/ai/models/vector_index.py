"""ai_vector_index ORM per ERD-27 Phase 2."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import VECTOR_INDEX_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in VECTOR_INDEX_STATUS_VALUES)


class AiVectorIndex(Base, *AiRowMixin):
    __tablename__ = "ai_vector_index"
    __table_args__ = (
        UniqueConstraint("company_id", "index_code", name="uk_ai_vector_index_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_vector_index_status",
        ),
        Index("ix_ai_vector_index_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_vector_index_kb", "knowledge_base_id"),
        Index("ix_ai_vector_index_model", "model_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    knowledge_base_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_knowledge_base.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    model_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_model.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    index_code: Mapped[str] = mapped_column(String(50), nullable=False)
    index_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    provider_index_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
