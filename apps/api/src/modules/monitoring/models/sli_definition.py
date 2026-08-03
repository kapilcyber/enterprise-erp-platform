"""mon_sli_definition ORM per ERD-29 Phase 3."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.monitoring.domain.enums import SLI_DEFINITION_STATUS_VALUES
from modules.monitoring.models.mixins import MonitoringRowMixin

_STATUSES = ",".join(f"'{t}'" for t in SLI_DEFINITION_STATUS_VALUES)


class MonSliDefinition(Base, *MonitoringRowMixin):
    __tablename__ = "mon_sli_definition"
    __table_args__ = (
        UniqueConstraint(
            "slo_id",
            "sli_code",
            "definition_version",
            name="uk_mon_sli_definition_code_ver",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_mon_sli_definition_status"),
        Index(
            "ix_mon_sli_definition_tenant_co_status",
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
    slo_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_slo_definition.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    sli_code: Mapped[str] = mapped_column(String(64), nullable=False)
    sli_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    indicator_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    metric_definition_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("monitoring.mon_metric_definition.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    definition_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
