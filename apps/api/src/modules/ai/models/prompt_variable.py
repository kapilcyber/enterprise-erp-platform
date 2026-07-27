"""ai_prompt_variable ORM per ERD-27 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import PROMPT_VARIABLE_DATA_TYPE_VALUES
from modules.ai.models.mixins import AiRowMixin

_DATA_TYPES = ",".join(f"'{t}'" for t in PROMPT_VARIABLE_DATA_TYPE_VALUES)


class AiPromptVariable(Base, *AiRowMixin):
    __tablename__ = "ai_prompt_variable"
    __table_args__ = (
        UniqueConstraint(
            "prompt_version_id", "variable_code", name="uk_ai_prompt_variable_code"
        ),
        CheckConstraint(
            f"data_type IN ({_DATA_TYPES})",
            name="ck_ai_prompt_variable_data_type",
        ),
        Index("ix_ai_prompt_variable_prompt_version", "prompt_version_id"),
        Index("ix_ai_prompt_variable_tenant_co", "tenant_id", "company_id"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    variable_code: Mapped[str] = mapped_column(String(50), nullable=False)
    variable_name: Mapped[str] = mapped_column(String(255), nullable=False)
    data_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    default_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    prompt_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_prompt_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
