"""lc_form_field ORM per ERD-26 Phase 2A · 2B · 2C.

Validation rules and bindings are merged onto this table (no separate entities).
Optional component_version_id references the Low-Code component catalog (Phase 2B).
Optional data_source_id references the Low-Code data source registry (Phase 2C).
"""

from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
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
from modules.lowcode.domain.enums import FIELD_TYPE_VALUES
from modules.lowcode.models.mixins import LowcodeRowMixin

_FIELD_TYPES = ",".join(f"'{t}'" for t in FIELD_TYPE_VALUES)


class LcFormField(Base, *LowcodeRowMixin):
    __tablename__ = "lc_form_field"
    __table_args__ = (
        UniqueConstraint(
            "form_version_id", "field_key", name="uk_lc_form_field_key"
        ),
        UniqueConstraint(
            "form_version_id", "field_code", name="uk_lc_form_field_code"
        ),
        CheckConstraint(
            f"field_type IN ({_FIELD_TYPES})",
            name="ck_lc_form_field_type",
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_lc_form_field_status",
        ),
        CheckConstraint(
            "display_order >= 0",
            name="ck_lc_form_field_display_order",
        ),
        Index("ix_lc_form_field_form_version", "form_version_id"),
        Index("ix_lc_form_field_section", "section_id"),
        Index("ix_lc_form_field_component_version", "component_version_id"),
        Index("ix_lc_form_field_data_source", "data_source_id"),
        Index("ix_lc_form_field_tenant_co", "tenant_id", "company_id"),
        Index("ix_lc_form_field_version_order", "form_version_id", "display_order"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    field_code: Mapped[str] = mapped_column(String(50), nullable=False)
    field_key: Mapped[str] = mapped_column(String(100), nullable=False)
    field_label: Mapped[str] = mapped_column(String(255), nullable=False)
    field_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    help_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    placeholder: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_readonly: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    form_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    section_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_section.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Optional catalog component version (ERD-26); no peer module ORM
    component_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_component_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    # Optional data source registry ref (ERD-26 Phase 2C); contract metadata only
    data_source_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_data_source.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    # Merged validation + binding metadata (JSON text); no peer ORM
    validation_rules_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    binding_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    options_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Attachment fields may reference Document UUID only (no Document FK)
    document_ref_uuid: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True
    )
