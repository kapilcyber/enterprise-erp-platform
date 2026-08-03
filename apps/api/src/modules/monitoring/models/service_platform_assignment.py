"""mon_service_platform_assignment ORM per ERD-29 Phase 3."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.monitoring.domain.enums import ASSIGNMENT_STATUS_VALUES
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in ASSIGNMENT_STATUS_VALUES)


class MonServicePlatformAssignment(Base, *MonitoringRowMixin):
    __tablename__ = "mon_service_platform_assignment"
    __table_args__ = (
        UniqueConstraint(
            "service_id",
            "component_id",
            "platform_binding_id",
            name="uk_mon_service_platform_assignment",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})", name="ck_mon_service_platform_assignment_status"
        ),
        Index(
            "ix_mon_svc_plat_assign_tenant_co_status",
            "tenant_id",
            "company_id",
            "status",
        ),
        {"schema": "monitoring"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    branch_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organization.org_branch.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    service_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_monitored_service.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    component_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_monitored_component.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    platform_binding_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_external_platform_binding.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    assignment_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    hub_projection_ref: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
