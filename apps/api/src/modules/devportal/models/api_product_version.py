"""dp_api_product_version ORM per ERD-28 Phase 1 — Draft / Published / Retired; published immutable."""  # noqa: E501

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import API_PRODUCT_VERSION_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in API_PRODUCT_VERSION_STATUS_VALUES)


class DpApiProductVersion(Base, *DevportalRowMixin):
    __tablename__ = "dp_api_product_version"
    __table_args__ = (
        UniqueConstraint("company_id", "product_id", "version_label", name="uk_dp_api_product_version_label"),  # noqa: E501
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_api_product_version_status"),
        Index("ix_dp_api_product_version_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_api_product_version_product", "product_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_api_product.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    version_label: Mapped[str] = mapped_column(String(50), nullable=False)
    changelog_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
