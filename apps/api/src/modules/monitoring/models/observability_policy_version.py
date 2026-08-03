"""mon_observability_policy_version ORM per ERD-29 Phase 1."""

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
from modules.monitoring.domain.enums import OBSERVABILITY_POLICY_VERSION_STATUS_VALUES
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in OBSERVABILITY_POLICY_VERSION_STATUS_VALUES)


class MonObservabilityPolicyVersion(Base, *MonitoringRowMixin):
    __tablename__ = "mon_observability_policy_version"
    __table_args__ = (
        UniqueConstraint(
            "policy_id",
            "version_label",
            name="uk_mon_obs_policy_version_label",
        ),
        UniqueConstraint(
            "policy_id",
            "version_number",
            name="uk_mon_obs_policy_version_number",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})", name="ck_mon_obs_policy_version_status"
        ),
        Index("ix_mon_obs_policy_ver_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_mon_obs_policy_ver_policy_status", "policy_id", "status"),
        {"schema": "monitoring"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    branch_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organization.org_branch.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    policy_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_observability_policy.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    version_label: Mapped[str] = mapped_column(String(32), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    retention_intent_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    sampling_intent_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    redaction_policy_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    content_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    change_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
