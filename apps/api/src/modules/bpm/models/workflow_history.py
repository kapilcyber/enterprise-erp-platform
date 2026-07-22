"""bpm_workflow_history ORM per ERD-25 Phase 4 — append-only audit trail."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import HISTORY_EVENT_TYPE_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_EVENTS = ",".join(f"'{t}'" for t in HISTORY_EVENT_TYPE_VALUES)


class BpmWorkflowHistory(Base, *BpmRowMixin):
    __tablename__ = "bpm_workflow_history"
    __table_args__ = (
        CheckConstraint(
            f"event_type IN ({_EVENTS})",
            name="ck_bpm_workflow_history_event_type",
        ),
        Index("ix_bpm_workflow_history_instance", "instance_id"),
        Index("ix_bpm_workflow_history_task", "task_id"),
        Index("ix_bpm_workflow_history_event", "event_type"),
        Index("ix_bpm_workflow_history_occurred", "occurred_at"),
        Index("ix_bpm_workflow_history_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_code: Mapped[str] = mapped_column(String(50), nullable=False)
    event_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    from_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    to_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    actor_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True, index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    instance_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_instance.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    task_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_task.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    delegation_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        index=True,
    )
