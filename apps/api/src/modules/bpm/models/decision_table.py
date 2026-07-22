"""bpm_decision_table ORM per ERD-25 Phase 2B."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.models.mixins import BpmRowMixin


class BpmDecisionTable(Base, *BpmRowMixin):
    __tablename__ = "bpm_decision_table"
    __table_args__ = (
        UniqueConstraint("version_id", "table_code", name="uk_bpm_decision_table_code"),
        CheckConstraint(
            "status IN ('enabled','disabled')",
            name="ck_bpm_decision_table_status",
        ),
        Index("ix_bpm_decision_table_version", "version_id"),
        Index("ix_bpm_decision_table_version_status", "version_id", "status"),
        Index("ix_bpm_decision_table_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    table_code: Mapped[str] = mapped_column(String(50), nullable=False)
    table_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="enabled", index=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    evaluation_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Row management stored as JSON array (no separate ERD row table)
    rows_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
