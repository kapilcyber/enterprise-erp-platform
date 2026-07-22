"""bpm_escalation_policy ORM per ERD-25 Phase 3A."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import ESCALATION_TARGET_TYPE_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_TARGETS = ",".join(f"'{t}'" for t in ESCALATION_TARGET_TYPE_VALUES)


class BpmEscalationPolicy(Base, *BpmRowMixin):
    __tablename__ = "bpm_escalation_policy"
    __table_args__ = (
        UniqueConstraint("version_id", "policy_code", name="uk_bpm_escalation_policy_code"),
        CheckConstraint(
            f"escalation_target_type IN ({_TARGETS})",
            name="ck_bpm_escalation_policy_target_type",
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_bpm_escalation_policy_status",
        ),
        CheckConstraint(
            "escalation_level >= 1",
            name="ck_bpm_escalation_policy_level",
        ),
        CheckConstraint(
            "escalation_delay_minutes >= 0",
            name="ck_bpm_escalation_policy_delay",
        ),
        CheckConstraint(
            "retry_count >= 0",
            name="ck_bpm_escalation_policy_retry",
        ),
        Index("ix_bpm_escalation_policy_version", "version_id"),
        Index("ix_bpm_escalation_policy_node", "node_id"),
        Index("ix_bpm_escalation_policy_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    policy_code: Mapped[str] = mapped_column(String(50), nullable=False)
    policy_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)

    escalation_level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    escalation_delay_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    escalation_target_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    escalation_target_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, index=True
    )
    escalation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Multi-level escalation ladder (JSON array of level specs)
    levels_json: Mapped[str | None] = mapped_column(Text, nullable=True)

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
