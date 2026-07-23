"""lc_runtime_submission ORM per ERD-26 Phase 4 — correlation envelope only."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.lowcode.domain.enums import SUBMISSION_STATUS_VALUES
from modules.lowcode.models.mixins import LowcodeRowMixin

_STATUSES = ",".join(f"'{t}'" for t in SUBMISSION_STATUS_VALUES)


class LcRuntimeSubmission(Base, *LowcodeRowMixin):
    __tablename__ = "lc_runtime_submission"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "submission_code", name="uk_lc_runtime_submission_code"
        ),
        UniqueConstraint(
            "company_id", "correlation_id", name="uk_lc_runtime_submission_correlation"
        ),
        CheckConstraint(
            f"submission_status IN ({_STATUSES})",
            name="ck_lc_runtime_submission_status",
        ),
        Index("ix_lc_runtime_submission_form_version", "form_version_id"),
        Index("ix_lc_runtime_submission_page_version", "page_version_id"),
        Index("ix_lc_runtime_submission_module_entity", "module_code", "entity_id"),
        Index("ix_lc_runtime_submission_bpm_task", "bpm_task_id"),
        Index("ix_lc_runtime_submission_tenant_co", "tenant_id", "company_id"),
        {"schema": "lowcode"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    submission_code: Mapped[str] = mapped_column(String(50), nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(100), nullable=False)
    submission_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="received", index=True
    )

    # Published design versions (UUID refs within Low-Code only)
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

    # Business context — UUID + module code only; no peer ORM / no business SoR
    module_code: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    bpm_task_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)

    validation_result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Correlation snapshot prior to handoff — never business SoR
    field_values_snapshot_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
