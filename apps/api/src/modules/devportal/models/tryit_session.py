"""dp_tryit_session ORM per ERD-28 Phase 3 — metadata only; no live API invoke."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import TRYIT_SESSION_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in TRYIT_SESSION_STATUS_VALUES)


class DpTryitSession(Base, *DevportalRowMixin):
    __tablename__ = "dp_tryit_session"
    __table_args__ = (
        UniqueConstraint("company_id", "session_code", name="uk_dp_tryit_session_code"),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_tryit_session_status"),
        Index("ix_dp_tryit_session_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_tryit_session_sandbox", "sandbox_environment_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_code: Mapped[str] = mapped_column(String(50), nullable=False)
    sandbox_environment_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_sandbox_environment.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    application_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_application.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    product_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_api_product_version.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
