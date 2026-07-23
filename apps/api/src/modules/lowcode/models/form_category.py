"""lc_form_category ORM per ERD-26 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.models.mixins import LowcodeRowMixin


class LcFormCategory(Base, *LowcodeRowMixin):
    __tablename__ = "lc_form_category"
    __table_args__ = (
        UniqueConstraint("company_id", "category_code", name="uk_lc_form_category_code"),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_lc_form_category_status",
        ),
        Index("ix_lc_form_category_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_lc_form_category_name_search", "company_id", "category_name"),
        Index("ix_lc_form_category_code_search", "company_id", "category_code"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    category_code: Mapped[str] = mapped_column(String(50), nullable=False)
    category_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
