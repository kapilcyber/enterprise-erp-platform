"""mon_alert_routing_policy ORM per ERD-29 Phase 2."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
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
from modules.monitoring.domain.enums import ALERT_ROUTING_POLICY_STATUS_VALUES
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in ALERT_ROUTING_POLICY_STATUS_VALUES)


class MonAlertRoutingPolicy(Base, *MonitoringRowMixin):
    __tablename__ = "mon_alert_routing_policy"
    __table_args__ = (
        UniqueConstraint(
            "alert_rule_id",
            "routing_code",
            "definition_version",
            name="uk_mon_alert_routing_policy_code_ver",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_mon_alert_routing_policy_status"),
        Index(
            "ix_mon_alert_routing_policy_tenant_co_status",
            "tenant_id",
            "company_id",
            "status",
        ),
        Index("ix_mon_alert_routing_policy_channel_ref", "notification_channel_ref"),
        {"schema": "monitoring"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    branch_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organization.org_branch.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    alert_rule_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_alert_rule.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    routing_code: Mapped[str] = mapped_column(String(64), nullable=False)
    routing_name: Mapped[str] = mapped_column(String(255), nullable=False)
    notification_channel_ref: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False
    )
    channel_kind: Mapped[str | None] = mapped_column(String(40), nullable=True)
    routing_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_critical_route: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    definition_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
