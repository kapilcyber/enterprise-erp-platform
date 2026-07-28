"""dp_developer_membership ORM per ERD-28 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import MEMBERSHIP_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in MEMBERSHIP_STATUS_VALUES)


class DpDeveloperMembership(Base, *DevportalRowMixin):
    __tablename__ = "dp_developer_membership"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "account_id", "organization_id", "team_id",
            name="uk_dp_developer_membership_scope",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_developer_membership_status"),
        Index("ix_dp_developer_membership_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_developer_membership_account", "account_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_developer_account.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_developer_organization.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    team_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_developer_team.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    membership_role: Mapped[str] = mapped_column(String(50), nullable=False, default="member")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
