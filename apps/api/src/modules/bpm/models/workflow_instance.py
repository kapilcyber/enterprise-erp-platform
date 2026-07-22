"""bpm_workflow_instance ORM per ERD-25 Phase 4 — Published version runtime only."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import INSTANCE_STATUS_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_STATUSES = ",".join(f"'{t}'" for t in INSTANCE_STATUS_VALUES)


class BpmWorkflowInstance(Base, *BpmRowMixin):
    __tablename__ = "bpm_workflow_instance"
    __table_args__ = (
        UniqueConstraint("instance_code", "tenant_id", name="uk_bpm_workflow_instance_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_bpm_workflow_instance_status",
        ),
        Index("ix_bpm_workflow_instance_version", "version_id"),
        Index("ix_bpm_workflow_instance_definition", "definition_id"),
        Index("ix_bpm_workflow_instance_business", "module_code", "entity_id"),
        Index("ix_bpm_workflow_instance_status", "status"),
        Index("ix_bpm_workflow_instance_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    instance_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending", index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Business SoR reference — UUID only (no peer FK / ORM write)
    module_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    entity_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)

    context_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    cancel_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    suspended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    definition_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_definition.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    started_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
