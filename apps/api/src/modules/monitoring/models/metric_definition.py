"""mon_metric_definition ORM per ERD-29 Phase 1."""

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
    METRIC_DEFINITION_STATUS_VALUES,
    METRIC_TYPE_VALUES,
)
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in METRIC_DEFINITION_STATUS_VALUES)
_TYPES = ",".join(f"'{t}'" for t in METRIC_TYPE_VALUES)


class MonMetricDefinition(Base, *MonitoringRowMixin):
    __tablename__ = "mon_metric_definition"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "company_id",
            "metric_code",
            "definition_version",
            name="uk_mon_metric_definition_code_ver",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_mon_metric_definition_status"),
        CheckConstraint(f"metric_type IN ({_TYPES})", name="ck_mon_metric_definition_type"),
        Index("ix_mon_metric_def_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_mon_metric_def_metric_code", "metric_code"),
        {"schema": "monitoring"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    branch_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organization.org_branch.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    metric_code: Mapped[str] = mapped_column(String(128), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    metric_type: Mapped[str] = mapped_column(String(40), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(40), nullable=True)
    label_schema_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    definition_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
