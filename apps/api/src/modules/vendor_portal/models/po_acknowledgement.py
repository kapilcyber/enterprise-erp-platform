"""Vendor Portal ORM — vp_po_acknowledgement per ERD_24."""

from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    Date,
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


class VpPoAcknowledgement(Base, *VpRowMixin):
    __tablename__ = "vp_po_acknowledgement"
    __table_args__ = (
        UniqueConstraint("company_id", "ack_number", name="uk_vp_po_acknowledgement_ack_number"),
        CheckConstraint(
            "status IN ('draft','submitted','acknowledged','disputed','cancelled')",
            name="ck_vp_po_acknowledgement_status",
        ),
        Index("ix_vp_po_acknowledgement_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    ack_number: Mapped[str] = mapped_column(String(50), nullable=False)
    portal_account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendor_portal.vp_portal_account.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    purchase_order_view_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendor_portal.vp_purchase_order_view.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    proc_order_header_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    ack_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
    confirmed_delivery_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    change_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_by_employee_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("master.master_employee.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    workflow_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("foundation.wf_instance.id", ondelete="SET NULL"),
        nullable=True,
    )

