"""Vendor Portal ORM — vp_dashboard per ERD_24."""

from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.vendor_portal.models.mixins import VpRowMixin


class VpDashboard(Base, *VpRowMixin):
    __tablename__ = "vp_dashboard"
    __table_args__ = (
        UniqueConstraint("company_id", "dashboard_number", name="uk_vp_dashboard_dashboard_number"),
        CheckConstraint(
            "status IN ('draft','active','archived')",
            name="ck_vp_dashboard_status",
        ),
        Index("ix_vp_dashboard_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    dashboard_number: Mapped[str] = mapped_column(String(50), nullable=False)
    portal_account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendor_portal.vp_portal_account.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    dashboard_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    dashboard_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    layout_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

