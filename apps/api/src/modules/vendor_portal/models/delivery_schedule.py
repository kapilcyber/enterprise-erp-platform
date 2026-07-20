"""Vendor Portal ORM — vp_delivery_schedule per ERD_24."""

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


class VpDeliverySchedule(Base, *VpRowMixin):
    __tablename__ = "vp_delivery_schedule"
    __table_args__ = (
        UniqueConstraint("company_id", "schedule_number", name="uk_vp_delivery_schedule_schedule_number"),  # noqa: E501
        CheckConstraint(
            "status IN ('planned','confirmed','partially_shipped','completed','cancelled')",
            name="ck_vp_delivery_schedule_status",
        ),
        Index("ix_vp_delivery_schedule_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    schedule_number: Mapped[str] = mapped_column(String(50), nullable=False)
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
    proc_order_line_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    product_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("master.master_product.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    promised_qty: Mapped[float | None] = mapped_column(Numeric(18, 4), nullable=True)
    promised_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    ship_from_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="planned", index=True)

