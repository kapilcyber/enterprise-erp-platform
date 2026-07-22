"""bpm_form_reference ORM per ERD-25 Phase 2B — Low-Code form UUID only."""

from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import FORM_MODE_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_MODES = ",".join(f"'{t}'" for t in FORM_MODE_VALUES)


class BpmFormReference(Base, *BpmRowMixin):
    __tablename__ = "bpm_form_reference"
    __table_args__ = (
        UniqueConstraint(
            "version_id", "reference_code", name="uk_bpm_form_reference_code"
        ),
        CheckConstraint(
            f"access_mode IN ({_MODES})",
            name="ck_bpm_form_reference_mode",
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_bpm_form_reference_status",
        ),
        Index("ix_bpm_form_reference_version", "version_id"),
        Index("ix_bpm_form_reference_node", "node_id"),
        Index("ix_bpm_form_reference_low_code", "low_code_form_id"),
        Index("ix_bpm_form_reference_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    reference_code: Mapped[str] = mapped_column(String(50), nullable=False)
    reference_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    access_mode: Mapped[str] = mapped_column(
        String(30), nullable=False, default="editable", index=True
    )
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    validation_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Low-Code Platform owns forms — UUID reference only (no form definition ownership)
    low_code_form_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False, index=True
    )

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
