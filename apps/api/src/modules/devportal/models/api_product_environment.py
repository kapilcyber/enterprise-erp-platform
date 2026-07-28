"""dp_api_product_environment ORM per ERD-28 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import REGISTRY_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in REGISTRY_STATUS_VALUES)


class DpApiProductEnvironment(Base, *DevportalRowMixin):
    __tablename__ = "dp_api_product_environment"
    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "product_version_id",
            "environment_code",
            name="uk_dp_api_product_environment_code",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_dp_api_product_environment_status",
        ),
        Index(
            "ix_dp_api_product_environment_tenant_co_status",
            "tenant_id",
            "company_id",
            "status",
        ),
        Index("ix_dp_api_product_environment_version", "product_version_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_api_product_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    environment_code: Mapped[str] = mapped_column(String(50), nullable=False)
    environment_name: Mapped[str] = mapped_column(String(255), nullable=False)
    base_url_hint: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
