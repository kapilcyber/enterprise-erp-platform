"""dp_openapi_artifact_reference ORM per ERD-28 Phase 3 — Document UUID refs only."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import OPENAPI_ARTIFACT_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in OPENAPI_ARTIFACT_STATUS_VALUES)


class DpOpenapiArtifactReference(Base, *DevportalRowMixin):
    __tablename__ = "dp_openapi_artifact_reference"
    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "product_version_id",
            "artifact_code",
            name="uk_dp_openapi_artifact_reference_code",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_dp_openapi_artifact_reference_status",
        ),
        Index(
            "ix_dp_openapi_artifact_reference_tenant_co_status",
            "tenant_id",
            "company_id",
            "status",
        ),
        Index("ix_dp_openapi_artifact_reference_product_version", "product_version_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_api_product_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    documentation_entry_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_documentation_entry.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    artifact_code: Mapped[str] = mapped_column(String(50), nullable=False)
    # Peer UUID — Document Management SoR; no binary storage; no peer FK
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    openapi_version: Mapped[str | None] = mapped_column(String(30), nullable=True)
    snapshot_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    snapshot_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
