"""lc_data_source ORM per ERD-26 Phase 2C — contract registry only."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.models.mixins import LowcodeRowMixin


class LcDataSource(Base, *LowcodeRowMixin):
    __tablename__ = "lc_data_source"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "data_source_code", name="uk_lc_data_source_code"
        ),
        CheckConstraint(
            "status IN ('draft','active','retired')",
            name="ck_lc_data_source_status",
        ),
        Index("ix_lc_data_source_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_lc_data_source_module_entity", "module_code", "entity_type"),
        Index("ix_lc_data_source_name_search", "company_id", "data_source_name"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    data_source_code: Mapped[str] = mapped_column(String(50), nullable=False)
    data_source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    # Module contract metadata only — never stores business rows
    module_code: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # Comma or JSON list of allowed ops: read, write, lookup
    allowed_operations: Mapped[str] = mapped_column(
        String(100), nullable=False, default="read,lookup"
    )
    attribute_catalog_json: Mapped[str | None] = mapped_column(Text, nullable=True)
