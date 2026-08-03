"""mon_log_trace_policy ORM per ERD-29 Phase 2."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.monitoring.domain.enums import (
    LOG_TRACE_POLICY_STATUS_VALUES,
    SIGNAL_KIND_VALUES,
)
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in LOG_TRACE_POLICY_STATUS_VALUES)
_KINDS = ",".join(f"'{t}'" for t in SIGNAL_KIND_VALUES)


class MonLogTracePolicy(Base, *MonitoringRowMixin):
    __tablename__ = "mon_log_trace_policy"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "company_id",
            "policy_code",
            "definition_version",
            name="uk_mon_log_trace_policy_code_ver",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_mon_log_trace_policy_status"),
        CheckConstraint(f"signal_kind IN ({_KINDS})", name="ck_mon_log_trace_policy_kind"),
        Index(
            "ix_mon_log_trace_policy_tenant_co_kind_status",
            "tenant_id",
            "company_id",
            "signal_kind",
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
    policy_code: Mapped[str] = mapped_column(String(64), nullable=False)
    policy_name: Mapped[str] = mapped_column(String(255), nullable=False)
    signal_kind: Mapped[str] = mapped_column(String(20), nullable=False)
    policy_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_observability_policy_version.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    classification_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    sampling_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    redaction_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    retention_intent_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    definition_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
