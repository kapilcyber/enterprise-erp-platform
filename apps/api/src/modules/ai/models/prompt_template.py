"""ai_prompt_template ORM per ERD-27 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import PROMPT_TEMPLATE_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in PROMPT_TEMPLATE_STATUS_VALUES)


class AiPromptTemplate(Base, *AiRowMixin):
    __tablename__ = "ai_prompt_template"
    __table_args__ = (
        UniqueConstraint("company_id", "template_code", name="uk_ai_prompt_template_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_prompt_template_status",
        ),
        Index("ix_ai_prompt_template_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_prompt_template_name_search", "company_id", "template_name"),
        Index("ix_ai_prompt_template_code_search", "company_id", "template_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    template_code: Mapped[str] = mapped_column(String(50), nullable=False)
    template_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
