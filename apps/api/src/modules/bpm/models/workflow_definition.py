"""bpm_workflow_definition ORM per ERD-25 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.models.mixins import BpmRowMixin


class BpmWorkflowDefinition(Base, *BpmRowMixin):
    __tablename__ = "bpm_workflow_definition"
    __table_args__ = (
        UniqueConstraint("company_id", "definition_code", name="uk_bpm_workflow_definition_code"),
        CheckConstraint(
            "status IN ('draft','active','retired')",
            name="ck_bpm_workflow_definition_status",
        ),
        Index("ix_bpm_workflow_definition_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_bpm_workflow_definition_module_entity", "module_code", "entity_type"),
        Index("ix_bpm_workflow_definition_name_search", "company_id", "definition_name"),
        Index("ix_bpm_workflow_definition_code_search", "company_id", "definition_code"),
        Index("ix_bpm_workflow_definition_template", "template_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    definition_code: Mapped[str] = mapped_column(String(50), nullable=False)
    definition_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    template_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_template.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    module_code: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)

    owner_employee_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("master.master_employee.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    department_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organization.org_department.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
