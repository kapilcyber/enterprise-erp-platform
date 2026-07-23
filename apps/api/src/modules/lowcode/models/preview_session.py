"""lc_preview_session ORM per ERD-26 Phase 4 — design-time preview only."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.domain.enums import PREVIEW_MODE_VALUES, PREVIEW_SESSION_STATUS_VALUES
from modules.lowcode.models.mixins import LowcodeRowMixin

_MODES = ",".join(f"'{t}'" for t in PREVIEW_MODE_VALUES)
_STATUSES = ",".join(f"'{t}'" for t in PREVIEW_SESSION_STATUS_VALUES)


class LcPreviewSession(Base, *LowcodeRowMixin):
    __tablename__ = "lc_preview_session"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "session_code", name="uk_lc_preview_session_code"
        ),
        CheckConstraint(
            f"preview_mode IN ({_MODES})",
            name="ck_lc_preview_session_mode",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_lc_preview_session_status",
        ),
        Index("ix_lc_preview_session_form_version", "form_version_id"),
        Index("ix_lc_preview_session_page_version", "page_version_id"),
        Index("ix_lc_preview_session_designer", "designer_user_id"),
        Index("ix_lc_preview_session_expires", "expires_at"),
        Index("ix_lc_preview_session_tenant_co", "tenant_id", "company_id"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_code: Mapped[str] = mapped_column(String(50), nullable=False)
    preview_mode: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    designer_user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sample_context_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    form_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    page_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_page_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
