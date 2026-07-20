"""Vendor Portal ORM — vp_invoice_submission per ERD_24."""

from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.vendor_portal.models.mixins import VpRowMixin


class VpInvoiceSubmission(Base, *VpRowMixin):
    __tablename__ = "vp_invoice_submission"
    __table_args__ = (
        UniqueConstraint("company_id", "submission_number", name="uk_vp_invoice_submission_submission_number"),  # noqa: E501
        CheckConstraint(
            "status IN ('draft','submitted','under_review','accepted','rejected','withdrawn')",
            name="ck_vp_invoice_submission_status",
        ),
        Index("ix_vp_invoice_submission_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    submission_number: Mapped[str] = mapped_column(String(50), nullable=False)
    portal_account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendor_portal.vp_portal_account.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    vendor_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("master.master_vendor.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    purchase_order_view_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendor_portal.vp_purchase_order_view.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    proc_order_header_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    vendor_invoice_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)
    invoice_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    currency_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    total_amount: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    tax_amount: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    payload_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    proc_invoice_header_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
    )
    finance_ap_invoice_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    document_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
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

