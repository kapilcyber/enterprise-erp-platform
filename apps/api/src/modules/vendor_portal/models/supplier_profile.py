"""Vendor Portal ORM — vp_supplier_profile per ERD_24."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.vendor_portal.models.mixins import VpRowMixin


class VpSupplierProfile(Base, *VpRowMixin):
    __tablename__ = "vp_supplier_profile"
    __table_args__ = (
        UniqueConstraint("company_id", "profile_number", name="uk_vp_supplier_profile_profile_number"),  # noqa: E501
        CheckConstraint(
            "status IN ('draft','submitted','approved','active','inactive')",
            name="ck_vp_supplier_profile_status",
        ),
        Index("ix_vp_supplier_profile_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    profile_number: Mapped[str] = mapped_column(String(50), nullable=False)
    vendor_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("master.master_vendor.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    preferred_language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    primary_contact_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    remittance_contact_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    capabilities_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    workflow_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    workflow_instance_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("foundation.wf_instance.id", ondelete="SET NULL"),
        nullable=True,
    )

