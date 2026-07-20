"""Vendor Portal ORM — vp_login_audit per ERD_24."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.vendor_portal.models.mixins import VpRowMixin


class VpLoginAudit(Base, *VpRowMixin):
    __tablename__ = "vp_login_audit"
    __table_args__ = (
        UniqueConstraint("company_id", "audit_number", name="uk_vp_login_audit_audit_number"),
        CheckConstraint(
            "status IN ('recorded')",
            name="ck_vp_login_audit_status",
        ),
        Index("ix_vp_login_audit_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    audit_number: Mapped[str] = mapped_column(String(50), nullable=False)
    portal_account_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendor_portal.vp_portal_account.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
    occurred_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="recorded", index=True)

