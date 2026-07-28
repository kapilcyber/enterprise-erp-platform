"""dp_documentation_entry ORM per ERD-28 Phase 3 — guides/tutorials/changelog/release notes."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import (
    DOCUMENTATION_ENTRY_STATUS_VALUES,
    DOCUMENTATION_ENTRY_TYPE_VALUES,
)
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in DOCUMENTATION_ENTRY_STATUS_VALUES)
_TYPES = ",".join(f"'{t}'" for t in DOCUMENTATION_ENTRY_TYPE_VALUES)


class DpDocumentationEntry(Base, *DevportalRowMixin):
    __tablename__ = "dp_documentation_entry"
    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "product_version_id",
            "entry_code",
            name="uk_dp_documentation_entry_code",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_documentation_entry_status"),
        CheckConstraint(f"entry_type IN ({_TYPES})", name="ck_dp_documentation_entry_type"),
        Index("ix_dp_documentation_entry_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_documentation_entry_product_version", "product_version_id"),
        Index("ix_dp_documentation_entry_type", "entry_type"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_api_product_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    entry_code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    entry_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
