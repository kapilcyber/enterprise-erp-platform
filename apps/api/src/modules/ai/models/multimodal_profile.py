"""ai_multimodal_profile ORM per ERD-27 Phase 4 — integration readiness metadata only."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import (
    MULTIMODAL_MODALITY_VALUES,
    MULTIMODAL_PROFILE_STATUS_VALUES,
)
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in MULTIMODAL_PROFILE_STATUS_VALUES)
_MODALITIES = ",".join(f"'{t}'" for t in MULTIMODAL_MODALITY_VALUES)


class AiMultimodalProfile(Base, *AiRowMixin):
    __tablename__ = "ai_multimodal_profile"
    __table_args__ = (
        UniqueConstraint("company_id", "profile_code", name="uk_ai_multimodal_profile_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_multimodal_profile_status",
        ),
        CheckConstraint(
            f"modality_kind IN ({_MODALITIES})",
            name="ck_ai_multimodal_profile_modality",
        ),
        Index("ix_ai_multimodal_profile_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_multimodal_profile_provider", "provider_id"),
        Index("ix_ai_multimodal_profile_name_search", "company_id", "profile_name"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    profile_code: Mapped[str] = mapped_column(String(50), nullable=False)
    profile_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    modality_kind: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    capabilities_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    ingress_policy_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    egress_policy_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Document UUID ref only — no peer schema FK
    document_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    provider_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_provider.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    model_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_model.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    publish_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
