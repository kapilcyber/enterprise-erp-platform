"""mon_external_platform_binding ORM per ERD-29 Phase 3."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
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
    EXTERNAL_PLATFORM_BINDING_STATUS_VALUES,
    PLATFORM_TYPE_VALUES,
)
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in EXTERNAL_PLATFORM_BINDING_STATUS_VALUES)
_PLATFORMS = ",".join(f"'{t}'" for t in PLATFORM_TYPE_VALUES)


class MonExternalPlatformBinding(Base, *MonitoringRowMixin):
    __tablename__ = "mon_external_platform_binding"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "company_id",
            "binding_code",
            "definition_version",
            name="uk_mon_external_platform_binding_code_ver",
        ),
        CheckConstraint(
            f"status IN ({_STATUSES})", name="ck_mon_external_platform_binding_status"
        ),
        CheckConstraint(
            f"platform_type IN ({_PLATFORMS})", name="ck_mon_external_platform_binding_type"
        ),
        Index(
            "ix_mon_ext_plat_bind_tenant_co_type_status",
            "tenant_id",
            "company_id",
            "platform_type",
            "status",
        ),
        Index("ix_mon_ext_plat_bind_adapter_key", "adapter_key"),
        {"schema": "monitoring"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    branch_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organization.org_branch.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    binding_code: Mapped[str] = mapped_column(String(64), nullable=False)
    binding_name: Mapped[str] = mapped_column(String(255), nullable=False)
    platform_type: Mapped[str] = mapped_column(String(40), nullable=False)
    external_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    adapter_key: Mapped[str | None] = mapped_column(String(64), nullable=True)
    secret_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    endpoint_ref: Mapped[str | None] = mapped_column(String(512), nullable=True)
    binding_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    definition_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    activated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
