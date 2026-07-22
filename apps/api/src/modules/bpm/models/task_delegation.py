"""bpm_task_delegation ORM per ERD-25 Phase 4."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import DELEGATION_STATUS_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_STATUSES = ",".join(f"'{t}'" for t in DELEGATION_STATUS_VALUES)


class BpmTaskDelegation(Base, *BpmRowMixin):
    __tablename__ = "bpm_task_delegation"
    __table_args__ = (
        UniqueConstraint("task_id", "delegation_code", name="uk_bpm_task_delegation_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_bpm_task_delegation_status",
        ),
        Index("ix_bpm_task_delegation_task", "task_id"),
        Index("ix_bpm_task_delegation_original", "original_assignee_id"),
        Index("ix_bpm_task_delegation_delegate", "delegate_assignee_id"),
        Index("ix_bpm_task_delegation_status", "status"),
        Index("ix_bpm_task_delegation_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    delegation_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending", index=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    original_assignee_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False, index=True
    )
    delegate_assignee_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False, index=True
    )

    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    task_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_task.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
