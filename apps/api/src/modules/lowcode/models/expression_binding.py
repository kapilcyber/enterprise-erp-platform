"""lc_expression_binding ORM per ERD-26 Phase 2C."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.domain.enums import BINDING_TARGET_TYPE_VALUES
from modules.lowcode.models.mixins import LowcodeRowMixin

_TARGETS = ",".join(f"'{t}'" for t in BINDING_TARGET_TYPE_VALUES)


class LcExpressionBinding(Base, *LowcodeRowMixin):
    __tablename__ = "lc_expression_binding"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "binding_code", name="uk_lc_expression_binding_code"
        ),
        CheckConstraint(
            f"target_type IN ({_TARGETS})",
            name="ck_lc_expression_binding_target_type",
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_lc_expression_binding_status",
        ),
        CheckConstraint(
            "sort_order >= 0",
            name="ck_lc_expression_binding_sort_order",
        ),
        Index("ix_lc_expression_binding_expression", "expression_id"),
        Index("ix_lc_expression_binding_form_version", "form_version_id"),
        Index("ix_lc_expression_binding_section", "section_id"),
        Index("ix_lc_expression_binding_field", "field_id"),
        Index("ix_lc_expression_binding_tenant_co", "tenant_id", "company_id"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    binding_code: Mapped[str] = mapped_column(String(50), nullable=False)
    target_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    expression_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_expression.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Version-scoped targets (exactly one of these set per target_type)
    form_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    section_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_section.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    field_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_field.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    # Future page version — UUID only until page tables exist (no peer/page FK yet)
    page_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True
    )
