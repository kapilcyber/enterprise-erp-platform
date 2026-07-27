"""ai_provider_credential_reference ORM per ERD-27 Phase 1 — secret-store pointer only."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import CREDENTIAL_REFERENCE_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in CREDENTIAL_REFERENCE_STATUS_VALUES)


class AiProviderCredentialReference(Base, *AiRowMixin):
    __tablename__ = "ai_provider_credential_reference"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "credential_code", name="uk_ai_provider_credential_reference_code"
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_provider_credential_reference_status",
        ),
        Index("ix_ai_provider_credential_reference_provider", "provider_id"),
        Index("ix_ai_provider_credential_reference_tenant_co", "tenant_id", "company_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    credential_code: Mapped[str] = mapped_column(String(50), nullable=False)
    secret_store_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    provider_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_provider.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
