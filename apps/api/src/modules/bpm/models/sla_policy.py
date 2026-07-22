"""bpm_sla_policy ORM per ERD-25 Phase 3A."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.models.mixins import BpmRowMixin


class BpmSlaPolicy(Base, *BpmRowMixin):
    __tablename__ = "bpm_sla_policy"
    __table_args__ = (
        UniqueConstraint("version_id", "policy_code", name="uk_bpm_sla_policy_code"),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_bpm_sla_policy_status",
        ),
        CheckConstraint(
            "warning_threshold_minutes >= 0",
            name="ck_bpm_sla_policy_warning",
        ),
        CheckConstraint(
            "breach_threshold_minutes >= 0",
            name="ck_bpm_sla_policy_breach",
        ),
        Index("ix_bpm_sla_policy_version", "version_id"),
        Index("ix_bpm_sla_policy_node", "node_id"),
        Index("ix_bpm_sla_policy_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    policy_code: Mapped[str] = mapped_column(String(50), nullable=False)
    policy_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)

    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="UTC")
    business_hours_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    reminder_intervals_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    warning_threshold_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    breach_threshold_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=120)

    # Calendar / holiday calendar UUID references only (no ownership)
    calendar_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, index=True
    )
    holiday_calendar_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, index=True
    )

    version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    node_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_designer_node.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
