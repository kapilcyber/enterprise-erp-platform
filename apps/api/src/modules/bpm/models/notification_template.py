"""bpm_notification_template ORM per ERD-25 Phase 3B.

Defines WHAT content; Foundation Notification owns delivery (no delivery engine here).
"""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import NOTIFICATION_TEMPLATE_TYPE_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_TYPES = ",".join(f"'{t}'" for t in NOTIFICATION_TEMPLATE_TYPE_VALUES)


class BpmNotificationTemplate(Base, *BpmRowMixin):
    __tablename__ = "bpm_notification_template"
    __table_args__ = (
        UniqueConstraint(
            "version_id", "template_code", name="uk_bpm_notification_template_code"
        ),
        CheckConstraint(
            f"template_type IN ({_TYPES})",
            name="ck_bpm_notification_template_type",
        ),
        CheckConstraint(
            "status IN ('enabled','disabled')",
            name="ck_bpm_notification_template_status",
        ),
        Index("ix_bpm_notification_template_version", "version_id"),
        Index("ix_bpm_notification_template_type", "template_type"),
        Index("ix_bpm_notification_template_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    template_code: Mapped[str] = mapped_column(String(50), nullable=False)
    template_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="enabled", index=True)
    template_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)

    subject: Mapped[str | None] = mapped_column(String(500), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    variables_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    localization_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Optional Foundation Notification template UUID reference (delivery ownership external)
    foundation_template_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, index=True
    )

    version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
