"""dp_developer_invite ORM per ERD-28 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import DEVELOPER_INVITE_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in DEVELOPER_INVITE_STATUS_VALUES)


class DpDeveloperInvite(Base, *DevportalRowMixin):
    __tablename__ = "dp_developer_invite"
    __table_args__ = (
        UniqueConstraint("company_id", "invite_code", name="uk_dp_developer_invite_code"),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_developer_invite_status"),
        Index("ix_dp_developer_invite_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_developer_invite_org", "organization_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    invite_code: Mapped[str] = mapped_column(String(50), nullable=False)
    invite_email: Mapped[str] = mapped_column(String(255), nullable=False)
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
    account_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_developer_account.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    workflow_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    # Peer UUID — Foundation workflow instance; Foundation executes workflow
    workflow_instance_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
