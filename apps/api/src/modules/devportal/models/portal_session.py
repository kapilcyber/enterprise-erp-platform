"""dp_portal_session ORM per ERD-28 Phase 1 — metadata only; never replaces Foundation sessions."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import PORTAL_SESSION_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in PORTAL_SESSION_STATUS_VALUES)


class DpPortalSession(Base, *DevportalRowMixin):
    __tablename__ = "dp_portal_session"
    __table_args__ = (
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_portal_session_status"),
        Index("ix_dp_portal_session_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_portal_session_account", "account_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_developer_account.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    session_ref: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
