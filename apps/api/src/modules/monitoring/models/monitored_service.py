"""mon_monitored_service ORM per ERD-29 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.monitoring.domain.enums import (
    ENVIRONMENT_CLASS_VALUES,
    MONITORED_REGISTRY_STATUS_VALUES,
)
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in MONITORED_REGISTRY_STATUS_VALUES)
_ENVS = ",".join(f"'{t}'" for t in ENVIRONMENT_CLASS_VALUES)


class MonMonitoredService(Base, *MonitoringRowMixin):
    __tablename__ = "mon_monitored_service"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "company_id",
            "service_code",
            name="uk_mon_monitored_service_code",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_mon_monitored_service_status"),
        CheckConstraint(
            f"environment_class IN ({_ENVS})", name="ck_mon_monitored_service_env"
        ),
        Index("ix_mon_monitored_service_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_mon_monitored_service_module_code", "module_code"),
        Index("ix_mon_monitored_service_peer_module_ref", "peer_module_ref"),
        {"schema": "monitoring"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    branch_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organization.org_branch.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    service_code: Mapped[str] = mapped_column(String(64), nullable=False)
    service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    module_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    peer_module_ref: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    environment_class: Mapped[str] = mapped_column(
        String(30), nullable=False, default="production"
    )
    owner_ref: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
