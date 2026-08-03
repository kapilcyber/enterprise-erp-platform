"""mon_alert_rule ORM per ERD-29 Phase 2."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.monitoring.domain.enums import (
    ALERT_RULE_STATUS_VALUES,
    ALERT_SEVERITY_VALUES,
)
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in ALERT_RULE_STATUS_VALUES)
_SEVERITIES = ",".join(f"'{t}'" for t in ALERT_SEVERITY_VALUES)


class MonAlertRule(Base, *MonitoringRowMixin):
    __tablename__ = "mon_alert_rule"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "company_id",
            "rule_code",
            "definition_version",
            name="uk_mon_alert_rule_code_ver",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_mon_alert_rule_status"),
        CheckConstraint(f"severity IN ({_SEVERITIES})", name="ck_mon_alert_rule_severity"),
        Index(
            "ix_mon_alert_rule_tenant_co_sev_status",
            "tenant_id",
            "company_id",
            "severity",
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
    rule_code: Mapped[str] = mapped_column(String(64), nullable=False)
    rule_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="warning")
    metric_definition_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_metric_definition.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    # ERD: UUID attribute only — no ORM FK to mon_slo_definition (Phase 3 entity)
    slo_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    condition_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    definition_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
