"""bpm_simulation_run ORM per ERD-25 Phase 5 — no business mutation."""

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
from modules.bpm.domain.enums import SIMULATION_STATUS_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_STATUSES = ",".join(f"'{t}'" for t in SIMULATION_STATUS_VALUES)


class BpmSimulationRun(Base, *BpmRowMixin):
    __tablename__ = "bpm_simulation_run"
    __table_args__ = (
        UniqueConstraint("version_id", "simulation_code", name="uk_bpm_simulation_run_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_bpm_simulation_run_status",
        ),
        CheckConstraint(
            "duration_ms >= 0",
            name="ck_bpm_simulation_run_duration",
        ),
        Index("ix_bpm_simulation_run_version", "version_id"),
        Index("ix_bpm_simulation_run_status", "status"),
        Index("ix_bpm_simulation_run_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    simulation_code: Mapped[str] = mapped_column(String(50), nullable=False)
    simulation_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending", index=True)

    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    input_context_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    warnings_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    errors_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    execution_trace_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_summary_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    started_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
