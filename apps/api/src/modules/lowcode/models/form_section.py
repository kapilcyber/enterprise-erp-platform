"""lc_form_section ORM per ERD-26 Phase 2A."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.models.mixins import LowcodeRowMixin


class LcFormSection(Base, *LowcodeRowMixin):
    __tablename__ = "lc_form_section"
    __table_args__ = (
        UniqueConstraint(
            "form_version_id", "section_code", name="uk_lc_form_section_code"
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_lc_form_section_status",
        ),
        CheckConstraint(
            "display_order >= 0",
            name="ck_lc_form_section_display_order",
        ),
        Index("ix_lc_form_section_form_version", "form_version_id"),
        Index("ix_lc_form_section_tenant_co", "tenant_id", "company_id"),
        Index("ix_lc_form_section_version_order", "form_version_id", "display_order"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    section_code: Mapped[str] = mapped_column(String(50), nullable=False)
    section_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    form_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
