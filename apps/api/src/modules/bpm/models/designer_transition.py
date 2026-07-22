"""bpm_designer_transition ORM per ERD-25 Phase 2A."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import TRANSITION_TYPE_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_TRANSITION_TYPES = ",".join(f"'{t}'" for t in TRANSITION_TYPE_VALUES)


class BpmDesignerTransition(Base, *BpmRowMixin):
    __tablename__ = "bpm_designer_transition"
    __table_args__ = (
        UniqueConstraint(
            "version_id", "transition_code", name="uk_bpm_designer_transition_code"
        ),
        UniqueConstraint(
            "version_id",
            "from_node_id",
            "to_node_id",
            name="uk_bpm_designer_transition_edge",
        ),
        CheckConstraint(
            f"transition_type IN ({_TRANSITION_TYPES})",
            name="ck_bpm_designer_transition_type",
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_bpm_designer_transition_status",
        ),
        Index("ix_bpm_designer_transition_version", "version_id"),
        Index("ix_bpm_designer_transition_from", "from_node_id"),
        Index("ix_bpm_designer_transition_to", "to_node_id"),
        Index("ix_bpm_designer_transition_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    transition_code: Mapped[str] = mapped_column(String(50), nullable=False)
    transition_name: Mapped[str] = mapped_column(String(255), nullable=False)
    transition_type: Mapped[str] = mapped_column(
        String(40), nullable=False, default="sequential", index=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Conditional routing expression (designer-time only)
    condition_expression: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Decision table UUID reference only — table owned in later phase; no peer FK
    decision_table_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    from_node_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_designer_node.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    to_node_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_designer_node.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
