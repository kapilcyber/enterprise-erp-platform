"""lc_form_definition ORM per ERD-26 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.models.mixins import LowcodeRowMixin


class LcFormDefinition(Base, *LowcodeRowMixin):
    __tablename__ = "lc_form_definition"
    __table_args__ = (
        UniqueConstraint("company_id", "form_code", name="uk_lc_form_definition_code"),
        CheckConstraint(
            "status IN ('draft','active','retired')",
            name="ck_lc_form_definition_status",
        ),
        Index("ix_lc_form_definition_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_lc_form_definition_module", "module_affinity"),
        Index("ix_lc_form_definition_name_search", "company_id", "form_name"),
        Index("ix_lc_form_definition_code_search", "company_id", "form_code"),
        Index("ix_lc_form_definition_category", "category_id"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    form_code: Mapped[str] = mapped_column(String(50), nullable=False)
    form_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    category_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_category.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    # Module affinity for catalog search — UUID/service contracts only; no peer ORM
    module_affinity: Mapped[str] = mapped_column(String(50), nullable=False, default="general")
    entity_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
