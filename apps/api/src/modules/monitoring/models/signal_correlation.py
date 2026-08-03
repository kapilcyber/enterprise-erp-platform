"""mon_signal_correlation ORM per ERD-29 Phase 3."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.monitoring.domain.enums import SIGNAL_CORRELATION_STATUS_VALUES
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in SIGNAL_CORRELATION_STATUS_VALUES)


class MonSignalCorrelation(Base, *MonitoringRowMixin):
    __tablename__ = "mon_signal_correlation"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "company_id",
            "correlation_code",
            name="uk_mon_signal_correlation_code",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_mon_signal_correlation_status"),
        Index(
            "ix_mon_signal_correlation_tenant_co_status",
            "tenant_id",
            "company_id",
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
    correlation_code: Mapped[str] = mapped_column(String(64), nullable=False)
    correlation_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    alert_rule_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_alert_rule.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    metric_definition_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_metric_definition.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    correlation_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
