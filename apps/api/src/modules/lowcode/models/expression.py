"""lc_expression ORM per ERD-26 Phase 2C — UI expression definitions only."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.domain.enums import EXPRESSION_KIND_VALUES
from modules.lowcode.models.mixins import LowcodeRowMixin

_KINDS = ",".join(f"'{t}'" for t in EXPRESSION_KIND_VALUES)


class LcExpression(Base, *LowcodeRowMixin):
    __tablename__ = "lc_expression"
    __table_args__ = (
        UniqueConstraint("company_id", "expression_code", name="uk_lc_expression_code"),
        CheckConstraint(
            "status IN ('draft','published','retired')",
            name="ck_lc_expression_status",
        ),
        CheckConstraint(
            f"expression_kind IN ({_KINDS})",
            name="ck_lc_expression_kind",
        ),
        Index("ix_lc_expression_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_lc_expression_kind", "expression_kind"),
        Index("ix_lc_expression_name_search", "company_id", "expression_name"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    expression_code: Mapped[str] = mapped_column(String(50), nullable=False)
    expression_name: Mapped[str] = mapped_column(String(255), nullable=False)
    expression_kind: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Sandboxed UI expression body (metadata only — no runtime engine in Phase 2C)
    expression_body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    publish_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
