"""ai_context_package ORM per ERD-27 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.ai.domain.enums import CONTEXT_PACKAGE_STATUS_VALUES
from modules.ai.models.mixins import AiRowMixin

_STATUSES = ",".join(f"'{t}'" for t in CONTEXT_PACKAGE_STATUS_VALUES)


class AiContextPackage(Base, *AiRowMixin):
    __tablename__ = "ai_context_package"
    __table_args__ = (
        UniqueConstraint("company_id", "package_code", name="uk_ai_context_package_code"),
        CheckConstraint(
            f"status IN ({_STATUSES})",
            name="ck_ai_context_package_status",
        ),
        Index("ix_ai_context_package_session", "session_id"),
        Index("ix_ai_context_package_prompt_version", "prompt_version_id"),
        Index("ix_ai_context_package_module_entity", "module_code", "entity_id"),
        Index("ix_ai_context_package_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "ai"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    package_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    module_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    context_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_session.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    prompt_version_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("ai.ai_prompt_version.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    # Peer UUID refs only — no cross-schema FK
    lowcode_form_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    bpm_task_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    document_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
