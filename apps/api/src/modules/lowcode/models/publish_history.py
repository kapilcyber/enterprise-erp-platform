"""lc_publish_history ORM per ERD-26 Phase 4 — append-oriented operational trail."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.domain.enums import ARTIFACT_KIND_VALUES, PUBLISH_HISTORY_ACTION_VALUES
from modules.lowcode.models.mixins import LowcodeRowMixin

_ACTIONS = ",".join(f"'{t}'" for t in PUBLISH_HISTORY_ACTION_VALUES)
_KINDS = ",".join(f"'{t}'" for t in ARTIFACT_KIND_VALUES)


class LcPublishHistory(Base, *LowcodeRowMixin):
    __tablename__ = "lc_publish_history"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "history_code", name="uk_lc_publish_history_code"
        ),
        CheckConstraint(
            f"action IN ({_ACTIONS})",
            name="ck_lc_publish_history_action",
        ),
        CheckConstraint(
            f"artifact_kind IN ({_KINDS})",
            name="ck_lc_publish_history_artifact_kind",
        ),
        Index("ix_lc_publish_history_form_definition", "form_definition_id"),
        Index("ix_lc_publish_history_page_definition", "page_definition_id"),
        Index("ix_lc_publish_history_occurred", "occurred_at"),
        Index("ix_lc_publish_history_tenant_co", "tenant_id", "company_id"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    history_code: Mapped[str] = mapped_column(String(50), nullable=False)
    artifact_kind: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    performed_by: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)

    form_definition_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_form_definition.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    page_definition_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("lowcode.lc_page_definition.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    # Version transition UUIDs (form or page version ids — no cross-type FK)
    from_version_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    to_version_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
