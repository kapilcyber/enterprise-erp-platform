"""lc_component ORM per ERD-26 Phase 2B — stable catalog identity."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.domain.enums import COMPONENT_KIND_VALUES
from modules.lowcode.models.mixins import LowcodeRowMixin

_KINDS = ",".join(f"'{t}'" for t in COMPONENT_KIND_VALUES)


class LcComponent(Base, *LowcodeRowMixin):
    __tablename__ = "lc_component"
    __table_args__ = (
        UniqueConstraint("company_id", "component_code", name="uk_lc_component_code"),
        CheckConstraint(
            "status IN ('draft','active','retired')",
            name="ck_lc_component_status",
        ),
        CheckConstraint(
            f"component_kind IN ({_KINDS})",
            name="ck_lc_component_kind",
        ),
        Index("ix_lc_component_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_lc_component_kind", "component_kind"),
        Index("ix_lc_component_name_search", "company_id", "component_name"),
        Index("ix_lc_component_code_search", "company_id", "component_code"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    component_code: Mapped[str] = mapped_column(String(50), nullable=False)
    component_name: Mapped[str] = mapped_column(String(255), nullable=False)
    component_kind: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
