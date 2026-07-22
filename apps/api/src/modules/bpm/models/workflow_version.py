"""bpm_workflow_version ORM per ERD-25 Phase 1."""

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
from modules.bpm.models.mixins import BpmRowMixin


class BpmWorkflowVersion(Base, *BpmRowMixin):
    __tablename__ = "bpm_workflow_version"
    __table_args__ = (
        UniqueConstraint(
            "definition_id", "version_number", name="uk_bpm_workflow_version_number"
        ),
        CheckConstraint(
            "status IN ('draft','published','retired')",
            name="ck_bpm_workflow_version_status",
        ),
        Index("ix_bpm_workflow_version_definition_status", "definition_id", "status"),
        Index("ix_bpm_workflow_version_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    version_code: Mapped[str] = mapped_column(String(50), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    version_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    change_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    definition_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_definition.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    cloned_from_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Phase 1.5 audit polish — reasons (no new ERD table)
    publish_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    clone_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
