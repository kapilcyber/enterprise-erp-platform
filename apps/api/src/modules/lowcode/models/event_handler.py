"""lc_event_handler ORM per ERD-26 Phase 3A — event metadata only (no execution)."""

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
from modules.lowcode.domain.enums import BINDING_TARGET_TYPE_VALUES, EVENT_TYPE_VALUES
from modules.lowcode.models.mixins import LowcodeRowMixin

_EVENTS = ",".join(f"'{t}'" for t in EVENT_TYPE_VALUES)
_TARGETS = ",".join(f"'{t}'" for t in BINDING_TARGET_TYPE_VALUES)


class LcEventHandler(Base, *LowcodeRowMixin):
    __tablename__ = "lc_event_handler"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "handler_code", name="uk_lc_event_handler_code"
        ),
        CheckConstraint(
            f"event_type IN ({_EVENTS})",
            name="ck_lc_event_handler_event_type",
        ),
        CheckConstraint(
            f"target_type IN ({_TARGETS})",
            name="ck_lc_event_handler_target_type",
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_lc_event_handler_status",
        ),
        CheckConstraint(
            "execution_order >= 0",
            name="ck_lc_event_handler_execution_order",
        ),
        Index("ix_lc_event_handler_form_version", "form_version_id"),
        Index("ix_lc_event_handler_section", "section_id"),
        Index("ix_lc_event_handler_field", "field_id"),
        Index("ix_lc_event_handler_event_type", "event_type"),
        Index("ix_lc_event_handler_tenant_co", "tenant_id", "company_id"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    handler_code: Mapped[str] = mapped_column(String(50), nullable=False)
    # Trigger — FRD-26 / Phase 3A event catalog (metadata only)
    event_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    custom_event_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    target_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    execution_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # Handler contract metadata only — never executed by Low-Code in Phase 3A
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
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
    # Future page version — UUID only until page tables exist
    page_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True
    )
