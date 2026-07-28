"""dp_developer_account ORM per ERD-28 Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import DEVELOPER_ACCOUNT_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in DEVELOPER_ACCOUNT_STATUS_VALUES)


class DpDeveloperAccount(Base, *DevportalRowMixin):
    __tablename__ = "dp_developer_account"
    __table_args__ = (
        UniqueConstraint("company_id", "account_code", name="uk_dp_developer_account_code"),
        UniqueConstraint("company_id", "email", name="uk_dp_developer_account_email"),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_developer_account_status"),
        Index("ix_dp_developer_account_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_code: Mapped[str] = mapped_column(String(50), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    # Peer UUID — Foundation user SoR; no peer-schema FK
    foundation_user_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    workflow_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    # Peer UUID — Foundation workflow instance; no peer-schema FK
    workflow_instance_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
