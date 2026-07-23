"""lc_localization_entry ORM per ERD-26 Phase 3A — localization metadata only."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.domain.enums import LOCALIZATION_OWNER_TYPE_VALUES
from modules.lowcode.models.mixins import LowcodeRowMixin

_OWNERS = ",".join(f"'{t}'" for t in LOCALIZATION_OWNER_TYPE_VALUES)


class LcLocalizationEntry(Base, *LowcodeRowMixin):
    __tablename__ = "lc_localization_entry"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "entry_code", name="uk_lc_localization_entry_code"
        ),
        # Unique locale+key within owner scope (owner_ref_id = form/field/section/component/page id)
        UniqueConstraint(
            "owner_type",
            "owner_ref_id",
            "locale",
            "translation_key",
            name="uk_lc_localization_owner_locale_key",
        ),
        CheckConstraint(
            f"owner_type IN ({_OWNERS})",
            name="ck_lc_localization_owner_type",
        ),
        CheckConstraint(
            "status IN ('draft','published','retired')",
            name="ck_lc_localization_status",
        ),
        Index("ix_lc_localization_form_version", "form_version_id"),
        Index("ix_lc_localization_owner", "owner_type", "owner_ref_id"),
        Index("ix_lc_localization_locale", "locale"),
        Index("ix_lc_localization_tenant_co", "tenant_id", "company_id"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    entry_code: Mapped[str] = mapped_column(String(50), nullable=False)
    owner_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    # Stable owner identity for uniqueness
    # (form_version / field / section / component / page_version id)
    owner_ref_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    locale: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    translation_key: Mapped[str] = mapped_column(String(255), nullable=False)
    translated_value: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

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
    component_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_component.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    # Future page version — UUID only until page tables exist
    page_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    publish_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
