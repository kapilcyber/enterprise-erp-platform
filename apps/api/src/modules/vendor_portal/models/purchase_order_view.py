"""Vendor Portal ORM — vp_purchase_order_view per ERD_24."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.vendor_portal.models.mixins import VpRowMixin


class VpPurchaseOrderView(Base, *VpRowMixin):
    __tablename__ = "vp_purchase_order_view"
    __table_args__ = (
        UniqueConstraint("company_id", "view_number", name="uk_vp_purchase_order_view_view_number"),
        CheckConstraint(
            "status IN ('visible','hidden','stale','closed')",
            name="ck_vp_purchase_order_view_status",
        ),
        Index("ix_vp_purchase_order_view_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    view_number: Mapped[str] = mapped_column(String(50), nullable=False)
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
    proc_order_header_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    po_ref: Mapped[str | None] = mapped_column(String(100), nullable=True)
    po_status_text: Mapped[str | None] = mapped_column(String(50), nullable=True)
    product_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("master.master_product.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    ordered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    required_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="visible", index=True)

