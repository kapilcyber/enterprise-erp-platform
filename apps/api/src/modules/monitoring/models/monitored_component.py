"""mon_monitored_component ORM per ERD-29 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.monitoring.domain.enums import MONITORED_REGISTRY_STATUS_VALUES
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in MONITORED_REGISTRY_STATUS_VALUES)


class MonMonitoredComponent(Base, *MonitoringRowMixin):
    __tablename__ = "mon_monitored_component"
    __table_args__ = (
        UniqueConstraint(
            "service_id",
            "component_code",
            name="uk_mon_monitored_component_code",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_mon_monitored_component_status"),
        Index("ix_mon_monitored_component_tenant_co_status", "tenant_id", "company_id", "status"),
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
    component_code: Mapped[str] = mapped_column(String(64), nullable=False)
    component_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    component_kind: Mapped[str | None] = mapped_column(String(40), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
