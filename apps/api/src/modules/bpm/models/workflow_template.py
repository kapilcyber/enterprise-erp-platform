"""bpm_workflow_template ORM per ERD-25 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.models.mixins import BpmRowMixin


class BpmWorkflowTemplate(Base, *BpmRowMixin):
    __tablename__ = "bpm_workflow_template"
    __table_args__ = (
        UniqueConstraint("company_id", "template_code", name="uk_bpm_workflow_template_code"),
        CheckConstraint(
            "status IN ('draft','active','retired')",
            name="ck_bpm_workflow_template_status",
        ),
        Index("ix_bpm_workflow_template_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_bpm_workflow_template_category", "category_id"),
        Index("ix_bpm_workflow_template_name_search", "company_id", "template_name"),
        Index("ix_bpm_workflow_template_code_search", "company_id", "template_code"),
        Index("ix_bpm_workflow_template_module", "company_id", "module_code"),
        Index("ix_bpm_workflow_template_updated", "company_id", "updated_at"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    template_code: Mapped[str] = mapped_column(String(50), nullable=False)
    template_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    category_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_category.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    module_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    entity_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    owner_employee_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("master.master_employee.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
