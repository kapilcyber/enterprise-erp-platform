"""mon_observability_policy ORM per ERD-29 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.monitoring.domain.enums import (
    OBSERVABILITY_POLICY_STATUS_VALUES,
    POLICY_SCOPE_LEVEL_VALUES,
)
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in OBSERVABILITY_POLICY_STATUS_VALUES)
_SCOPES = ",".join(f"'{t}'" for t in POLICY_SCOPE_LEVEL_VALUES)


class MonObservabilityPolicy(Base, *MonitoringRowMixin):
    __tablename__ = "mon_observability_policy"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "company_id",
            "policy_code",
            name="uk_mon_observability_policy_code",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_mon_observability_policy_status"),
        CheckConstraint(f"scope_level IN ({_SCOPES})", name="ck_mon_observability_policy_scope"),
        Index("ix_mon_obs_policy_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_mon_obs_policy_created_at", "created_at"),
        {"schema": "monitoring"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    branch_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organization.org_branch.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    policy_code: Mapped[str] = mapped_column(String(64), nullable=False)
    policy_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    scope_level: Mapped[str] = mapped_column(String(30), nullable=False, default="platform")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
