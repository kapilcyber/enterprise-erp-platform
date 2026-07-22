"""bpm_workflow_variable ORM per ERD-25 Phase 2B."""

from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import VARIABLE_TYPE_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_VAR_TYPES = ",".join(f"'{t}'" for t in VARIABLE_TYPE_VALUES)


class BpmWorkflowVariable(Base, *BpmRowMixin):
    __tablename__ = "bpm_workflow_variable"
    __table_args__ = (
        UniqueConstraint("version_id", "variable_key", name="uk_bpm_workflow_variable_key"),
        CheckConstraint(
            f"variable_type IN ({_VAR_TYPES})",
            name="ck_bpm_workflow_variable_type",
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_bpm_workflow_variable_status",
        ),
        Index("ix_bpm_workflow_variable_version", "version_id"),
        Index("ix_bpm_workflow_variable_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    variable_key: Mapped[str] = mapped_column(String(100), nullable=False)
    variable_name: Mapped[str] = mapped_column(String(255), nullable=False)
    variable_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    default_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_encrypted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)

    version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
