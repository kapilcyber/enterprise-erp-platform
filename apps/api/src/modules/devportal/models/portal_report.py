"""dp_portal_report ORM per ERD-28 Phase 4 — operational report metadata only."""

from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Date, DateTime, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import (
    PORTAL_REPORT_STATUS_VALUES,
    PORTAL_REPORT_TYPE_VALUES,
)
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in PORTAL_REPORT_STATUS_VALUES)
_TYPES = ",".join(f"'{t}'" for t in PORTAL_REPORT_TYPE_VALUES)


class DpPortalReport(Base, *DevportalRowMixin):
    __tablename__ = "dp_portal_report"
    __table_args__ = (
        UniqueConstraint("company_id", "report_code", name="uk_dp_portal_report_code"),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_portal_report_status"),
        CheckConstraint(f"report_type IN ({_TYPES})", name="ck_dp_portal_report_type"),
        Index("ix_dp_portal_report_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_portal_report_type", "report_type"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    report_code: Mapped[str] = mapped_column(String(50), nullable=False)
    report_name: Mapped[str] = mapped_column(String(255), nullable=False)
    report_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    filters_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    config_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    export_preferences_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    schedule_metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    projection_snapshot_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    projected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    analytics_report_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, index=True
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    finalized_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finalized_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
