"""Vendor Portal ORM — vp_message per ERD_24."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.vendor_portal.models.mixins import VpRowMixin


class VpMessage(Base, *VpRowMixin):
    __tablename__ = "vp_message"
    __table_args__ = (
        UniqueConstraint("company_id", "message_number", name="uk_vp_message_message_number"),
        CheckConstraint(
            "status IN ('sent','delivered','read','deleted')",
            name="ck_vp_message_status",
        ),
        Index("ix_vp_message_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    message_number: Mapped[str] = mapped_column(String(50), nullable=False)
    message_thread_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendor_portal.vp_message_thread.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    sender_account_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendor_portal.vp_portal_account.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    sender_employee_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("master.master_employee.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="sent", index=True)

