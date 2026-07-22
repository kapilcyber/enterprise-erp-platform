"""bpm_workflow_task ORM per ERD-25 Phase 4."""

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
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import TASK_EXECUTION_MODE_VALUES, TASK_STATUS_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_STATUSES = ",".join(f"'{t}'" for t in TASK_STATUS_VALUES)
_MODES = ",".join(f"'{t}'" for t in TASK_EXECUTION_MODE_VALUES)


class BpmWorkflowTask(Base, *BpmRowMixin):
    __tablename__ = "bpm_workflow_task"
    __table_args__ = (
        UniqueConstraint("instance_id", "task_code", name="uk_bpm_workflow_task_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_bpm_workflow_task_status",
        ),
        CheckConstraint(
            f"execution_mode IN ({_MODES})",
            name="ck_bpm_workflow_task_execution_mode",
        ),
        Index("ix_bpm_workflow_task_instance", "instance_id"),
        Index("ix_bpm_workflow_task_assignee", "assignee_id"),
        Index("ix_bpm_workflow_task_status", "status"),
        Index("ix_bpm_workflow_task_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    task_code: Mapped[str] = mapped_column(String(50), nullable=False)
    task_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="open", index=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    execution_mode: Mapped[str] = mapped_column(
        String(30), nullable=False, default="sequential", index=True
    )
    parallel_group_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sequence_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    assignee_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, index=True
    )
    claimed_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    instance_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_instance.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    node_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_designer_node.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
