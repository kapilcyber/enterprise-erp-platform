"""dp_developer_team ORM per ERD-28 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import REGISTRY_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in REGISTRY_STATUS_VALUES)


class DpDeveloperTeam(Base, *DevportalRowMixin):
    __tablename__ = "dp_developer_team"
    __table_args__ = (
        UniqueConstraint("company_id", "organization_id", "team_code", name="uk_dp_developer_team_code"),  # noqa: E501
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_developer_team_status"),
        Index("ix_dp_developer_team_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_developer_team_org", "organization_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_developer_organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    team_code: Mapped[str] = mapped_column(String(50), nullable=False)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
