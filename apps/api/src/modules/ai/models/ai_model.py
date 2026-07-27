"""ai_model ORM per ERD-27 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import MODEL_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in MODEL_STATUS_VALUES)


class AiModel(Base, *AiRowMixin):
    __tablename__ = "ai_model"
    __table_args__ = (
        UniqueConstraint("company_id", "model_code", name="uk_ai_model_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_model_status",
        ),
        Index("ix_ai_model_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_model_provider", "provider_id"),
        Index("ix_ai_model_name_search", "company_id", "model_name"),
        Index("ix_ai_model_code_search", "company_id", "model_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_code: Mapped[str] = mapped_column(String(50), nullable=False)
    model_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    capability_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    residency_region: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cost_class: Mapped[str | None] = mapped_column(String(50), nullable=True)

    provider_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_provider.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
