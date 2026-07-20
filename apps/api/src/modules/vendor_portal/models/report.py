"""Vendor Portal ORM — vp_report per ERD_24."""

from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.vendor_portal.models.mixins import VpRowMixin


class VpReport(Base, *VpRowMixin):
    __tablename__ = "vp_report"
    __table_args__ = (
        UniqueConstraint("company_id", "report_code", name="uk_vp_report_code"),
        CheckConstraint(
            "status IN ('draft','finalized')",
            name="ck_vp_report_status",
        ),
        Index("ix_vp_report_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    report_code: Mapped[str] = mapped_column(String(50), nullable=False)
    report_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    metrics_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    generated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

