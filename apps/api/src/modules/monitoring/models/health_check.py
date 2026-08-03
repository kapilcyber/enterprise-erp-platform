"""mon_health_check ORM per ERD-29 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.monitoring.domain.enums import (
    HEALTH_CHECK_KIND_VALUES,
    HEALTH_CHECK_STATUS_VALUES,
)
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in HEALTH_CHECK_STATUS_VALUES)
_KINDS = ",".join(f"'{t}'" for t in HEALTH_CHECK_KIND_VALUES)


class MonHealthCheck(Base, *MonitoringRowMixin):
    __tablename__ = "mon_health_check"
    __table_args__ = (
        UniqueConstraint(
            "service_id",
            "check_code",
            name="uk_mon_health_check_code",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_mon_health_check_status"),
        CheckConstraint(f"check_kind IN ({_KINDS})", name="ck_mon_health_check_kind"),
        Index("ix_mon_health_check_tenant_co_status", "tenant_id", "company_id", "status"),
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
    check_code: Mapped[str] = mapped_column(String(64), nullable=False)
    check_name: Mapped[str] = mapped_column(String(255), nullable=False)
    check_kind: Mapped[str] = mapped_column(String(40), nullable=False, default="http")
    endpoint_ref: Mapped[str | None] = mapped_column(String(512), nullable=True)
    interval_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timeout_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    definition_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
