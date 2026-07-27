"""ai_tool ORM per ERD-27 Phase 3."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import TOOL_SIDE_EFFECT_CLASS_VALUES, TOOL_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in TOOL_STATUS_VALUES)
_SIDE_EFFECTS = ",".join(f"'{t}'" for t in TOOL_SIDE_EFFECT_CLASS_VALUES)


class AiTool(Base, *AiRowMixin):
    __tablename__ = "ai_tool"
    __table_args__ = (
        UniqueConstraint("company_id", "tool_code", name="uk_ai_tool_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_tool_status",
        ),
        CheckConstraint(
            f"side_effect_class IN ({_SIDE_EFFECTS})",
            name="ck_ai_tool_side_effect_class",
        ),
        Index("ix_ai_tool_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_tool_module_code", "company_id", "module_code"),
        Index("ix_ai_tool_name_search", "company_id", "tool_name"),
        Index("ix_ai_tool_code_search", "company_id", "tool_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tool_code: Mapped[str] = mapped_column(String(50), nullable=False)
    tool_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    module_code: Mapped[str] = mapped_column(String(100), nullable=False)
    side_effect_class: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    auth_scope_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retired_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    publish_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
