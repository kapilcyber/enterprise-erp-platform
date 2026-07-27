"""ai_configuration ORM per ERD-27 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import CONFIGURATION_SCOPE_VALUES, CONFIGURATION_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_SCOPES = ",".join(f"'{t}'" for t in CONFIGURATION_SCOPE_VALUES)
_STATUSES = ",".join(f"'{t}'" for t in CONFIGURATION_STATUS_VALUES)


class AiConfiguration(Base, *AiRowMixin):
    __tablename__ = "ai_configuration"
    __table_args__ = (
        UniqueConstraint("company_id", "config_code", name="uk_ai_configuration_code"),
        CheckConstraint(
            f"scope IN ({_SCOPES})",
            name="ck_ai_configuration_scope",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_configuration_status",
        ),
        Index("ix_ai_configuration_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_configuration_scope", "scope", "scope_ref_id"),
        Index("ix_ai_configuration_name_search", "company_id", "config_name"),
        Index("ix_ai_configuration_code_search", "company_id", "config_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    config_code: Mapped[str] = mapped_column(String(50), nullable=False)
    config_name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    scope_ref_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    config_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
