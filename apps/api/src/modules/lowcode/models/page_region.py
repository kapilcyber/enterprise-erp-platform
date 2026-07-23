"""lc_page_region ORM per ERD-26 Phase 3B — layout region metadata only."""

from uuid import UUID, uuid4

from sqlalchemy import (
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
from modules.lowcode.domain.enums import REGION_TYPE_VALUES
from modules.lowcode.models.mixins import LowcodeRowMixin

_REGION_TYPES = ",".join(f"'{t}'" for t in REGION_TYPE_VALUES)


class LcPageRegion(Base, *LowcodeRowMixin):
    __tablename__ = "lc_page_region"
    __table_args__ = (
        UniqueConstraint(
            "page_version_id", "region_code", name="uk_lc_page_region_code"
        ),
        CheckConstraint(
            f"region_type IN ({_REGION_TYPES})",
            name="ck_lc_page_region_type",
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_lc_page_region_status",
        ),
        CheckConstraint(
            "display_order >= 0",
            name="ck_lc_page_region_display_order",
        ),
        Index("ix_lc_page_region_page_version", "page_version_id"),
        Index("ix_lc_page_region_type", "region_type"),
        Index("ix_lc_page_region_form_version", "embedded_form_version_id"),
        Index("ix_lc_page_region_component_version", "embedded_component_version_id"),
        Index("ix_lc_page_region_tenant_co", "tenant_id", "company_id"),
        Index("ix_lc_page_region_version_order", "page_version_id", "display_order"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    region_code: Mapped[str] = mapped_column(String(50), nullable=False)
    region_name: Mapped[str] = mapped_column(String(255), nullable=False)
    region_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    page_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_page_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Layout metadata only — no rendering
    layout_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Embed by UUID reference only (Low-Code schema) — never duplicate form/component SoR
    embedded_form_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    embedded_component_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_component_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
