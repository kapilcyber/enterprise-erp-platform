"""bpm_assignment_rule ORM per ERD-25 Phase 3A — UUID refs only to Security/Org/Employee."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import ASSIGNMENT_STRATEGY_VALUES, ASSIGNMENT_TYPE_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_TYPES = ",".join(f"'{t}'" for t in ASSIGNMENT_TYPE_VALUES)
_STRATEGIES = ",".join(f"'{t}'" for t in ASSIGNMENT_STRATEGY_VALUES)


class BpmAssignmentRule(Base, *BpmRowMixin):
    __tablename__ = "bpm_assignment_rule"
    __table_args__ = (
        UniqueConstraint("version_id", "assignment_code", name="uk_bpm_assignment_rule_code"),
        CheckConstraint(
            f"assignment_type IN ({_TYPES})",
            name="ck_bpm_assignment_rule_type",
        ),
        CheckConstraint(
            f"strategy IN ({_STRATEGIES})",
            name="ck_bpm_assignment_rule_strategy",
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_bpm_assignment_rule_status",
        ),
        Index("ix_bpm_assignment_rule_version", "version_id"),
        Index("ix_bpm_assignment_rule_node", "node_id"),
        Index("ix_bpm_assignment_rule_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    assignment_code: Mapped[str] = mapped_column(String(50), nullable=False)
    assignment_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    assignment_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    strategy: Mapped[str] = mapped_column(String(40), nullable=False, default="static", index=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Cross-module UUID references only (no peer ORM ownership)
    role_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True, index=True)
    user_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True, index=True)
    department_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, index=True
    )
    employee_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, index=True
    )
    fallback_assignee_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, index=True
    )

    # Dynamic expression + round-robin / load-balance strategy metadata
    expression: Mapped[str | None] = mapped_column(Text, nullable=True)
    strategy_metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)

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
