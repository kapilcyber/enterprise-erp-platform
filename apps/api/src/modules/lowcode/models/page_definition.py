"""lc_page_definition ORM per ERD-26 Phase 3B — stable page identity."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.models.mixins import LowcodeRowMixin


class LcPageDefinition(Base, *LowcodeRowMixin):
    __tablename__ = "lc_page_definition"
    __table_args__ = (
        UniqueConstraint("company_id", "page_code", name="uk_lc_page_definition_code"),
        CheckConstraint(
            "status IN ('draft','active','retired')",
            name="ck_lc_page_definition_status",
        ),
        Index("ix_lc_page_definition_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_lc_page_definition_name_search", "company_id", "page_name"),
        Index("ix_lc_page_definition_code_search", "company_id", "page_code"),
        Index("ix_lc_page_definition_category", "category_id"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    page_code: Mapped[str] = mapped_column(String(50), nullable=False)
    page_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    # Optional taxonomy via existing Low-Code form category catalog
    category_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_category.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
