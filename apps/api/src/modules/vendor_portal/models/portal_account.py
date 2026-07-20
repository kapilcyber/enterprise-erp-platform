"""Vendor Portal ORM — vp_portal_account per ERD_24."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.vendor_portal.models.mixins import VpRowMixin


class VpPortalAccount(Base, *VpRowMixin):
    __tablename__ = "vp_portal_account"
    __table_args__ = (
        UniqueConstraint("company_id", "account_number", name="uk_vp_portal_account_account_number"),  # noqa: E501
        UniqueConstraint("company_id", "login_email", name="uk_vp_portal_account_login_email"),
        CheckConstraint(
            "status IN ('draft','submitted','approved','active','locked','suspended','retired')",
            name="ck_vp_portal_account_status",
        ),
        Index("ix_vp_portal_account_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    account_number: Mapped[str] = mapped_column(String(50), nullable=False)
    login_email: Mapped[str] = mapped_column(String(255), nullable=False)
    vendor_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("master.master_vendor.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    supplier_profile_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    credential_vault_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    owner_employee_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("master.master_employee.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    department_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organization.org_department.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    workflow_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("foundation.wf_instance.id", ondelete="SET NULL"),
        nullable=True,
    )

