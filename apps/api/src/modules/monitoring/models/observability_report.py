"""mon_observability_report ORM per ERD-29 Phase 4."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.monitoring.domain.enums import (
    EXPORT_FORMAT_VALUES,
    OBSERVABILITY_REPORT_STATUS_VALUES,
    REPORT_KIND_VALUES,
)
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in OBSERVABILITY_REPORT_STATUS_VALUES)
_KINDS = ",".join(f"'{t}'" for t in REPORT_KIND_VALUES)
_FORMATS = ",".join(f"'{t}'" for t in EXPORT_FORMAT_VALUES)


class MonObservabilityReport(Base, *MonitoringRowMixin):
    __tablename__ = "mon_observability_report"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "company_id",
            "report_code",
            name="uk_mon_observability_report_code",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})", name="ck_mon_observability_report_status"
        ),
        CheckConstraint(
            f"report_kind IN ({_KINDS})", name="ck_mon_observability_report_kind"
        ),
        CheckConstraint(
            f"export_format IS NULL OR export_format IN ({_FORMATS})",
            name="ck_mon_observability_report_export_format",
        ),
        Index(
            "ix_mon_observability_report_tenant_co_kind_status",
            "tenant_id",
            "company_id",
            "report_kind",
            "status",
        ),
        {"schema": "monitoring"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    branch_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organization.org_branch.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    report_code: Mapped[str] = mapped_column(String(64), nullable=False)
    report_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    report_kind: Mapped[str] = mapped_column(String(40), nullable=False, default="operational")
    definition_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    last_generated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    export_format: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
