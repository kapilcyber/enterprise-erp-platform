"""bpm_workflow_trigger ORM per ERD-25 Phase 3B.

Definition owns trigger capability; optional version binding is the active implementation.
"""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import TRIGGER_TYPE_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_TYPES = ",".join(f"'{t}'" for t in TRIGGER_TYPE_VALUES)


class BpmWorkflowTrigger(Base, *BpmRowMixin):
    __tablename__ = "bpm_workflow_trigger"
    __table_args__ = (
        UniqueConstraint("definition_id", "trigger_code", name="uk_bpm_workflow_trigger_code"),
        CheckConstraint(
            f"trigger_type IN ({_TYPES})",
            name="ck_bpm_workflow_trigger_type",
        ),
        CheckConstraint(
            "status IN ('enabled','disabled')",
            name="ck_bpm_workflow_trigger_status",
        ),
        Index("ix_bpm_workflow_trigger_definition", "definition_id"),
        Index("ix_bpm_workflow_trigger_version", "version_id"),
        Index("ix_bpm_workflow_trigger_type", "trigger_type"),
        Index("ix_bpm_workflow_trigger_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    trigger_code: Mapped[str] = mapped_column(String(50), nullable=False)
    trigger_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="enabled", index=True)
    trigger_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)

    event_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    module_code: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    entity_type: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    execution_mode_metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    definition_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_definition.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    # Optional active implementation binding on a version
    version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
