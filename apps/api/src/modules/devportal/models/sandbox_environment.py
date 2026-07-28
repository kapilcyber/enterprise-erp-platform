"""dp_sandbox_environment ORM per ERD-28 Phase 3 — metadata only; no runtime provisioning."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import SANDBOX_ENVIRONMENT_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in SANDBOX_ENVIRONMENT_STATUS_VALUES)


class DpSandboxEnvironment(Base, *DevportalRowMixin):
    __tablename__ = "dp_sandbox_environment"
    __table_args__ = (
        UniqueConstraint("company_id", "environment_code", name="uk_dp_sandbox_environment_code"),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_sandbox_environment_status"),
        Index("ix_dp_sandbox_environment_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    environment_code: Mapped[str] = mapped_column(String(50), nullable=False)
    environment_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    base_url_hint: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
