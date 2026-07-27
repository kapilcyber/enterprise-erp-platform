"""ai_cache_entry ORM per ERD-27 Phase 1 — cache metadata only (not SoR)."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import CACHE_ENTRY_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in CACHE_ENTRY_STATUS_VALUES)


class AiCacheEntry(Base, *AiRowMixin):
    __tablename__ = "ai_cache_entry"
    __table_args__ = (
        UniqueConstraint("company_id", "entry_code", name="uk_ai_cache_entry_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_cache_entry_status",
        ),
        Index("ix_ai_cache_entry_session", "session_id"),
        Index("ix_ai_cache_entry_cache_key", "cache_key"),
        Index("ix_ai_cache_entry_expires", "expires_at"),
        Index("ix_ai_cache_entry_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    entry_code: Mapped[str] = mapped_column(String(50), nullable=False)
    cache_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    cache_scope: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="created", index=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    session_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_session.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
