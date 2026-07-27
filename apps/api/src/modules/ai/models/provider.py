"""ai_provider ORM per ERD-27 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import PROVIDER_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in PROVIDER_STATUS_VALUES)


class AiProvider(Base, *AiRowMixin):
    __tablename__ = "ai_provider"
    __table_args__ = (
        UniqueConstraint("company_id", "provider_code", name="uk_ai_provider_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_provider_status",
        ),
        CheckConstraint(
            "sort_order >= 0",
            name="ck_ai_provider_sort_order",
        ),
        Index("ix_ai_provider_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_ai_provider_name_search", "company_id", "provider_name"),
        Index("ix_ai_provider_code_search", "company_id", "provider_code"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    provider_code: Mapped[str] = mapped_column(String(50), nullable=False)
    provider_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
