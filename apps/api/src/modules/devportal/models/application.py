"""dp_application ORM per ERD-28 Phase 1 — Hub UUID refs only; no secrets."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import APPLICATION_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in APPLICATION_STATUS_VALUES)


class DpApplication(Base, *DevportalRowMixin):
    __tablename__ = "dp_application"
    __table_args__ = (
        UniqueConstraint("company_id", "application_code", name="uk_dp_application_code"),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_application_status"),
        Index("ix_dp_application_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_application_account", "account_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_developer_account.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_developer_organization.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    application_code: Mapped[str] = mapped_column(String(50), nullable=False)
    application_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Peer UUIDs — Integration Hub SoR; never store secrets/gateway config
    oauth_client_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    api_credential_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    workflow_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
