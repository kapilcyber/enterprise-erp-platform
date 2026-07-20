"""Vendor Portal ORM — vp_preference per ERD_24."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.vendor_portal.models.mixins import VpRowMixin


class VpPreference(Base, *VpRowMixin):
    __tablename__ = "vp_preference"
    __table_args__ = (
        UniqueConstraint("portal_account_id", "preference_key", name="uk_vp_preference_key"),
        CheckConstraint(
            "status IN ('active')",
            name="ck_vp_preference_status",
        ),
        Index("ix_vp_preference_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    portal_account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendor_portal.vp_portal_account.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    preference_key: Mapped[str] = mapped_column(String(100), nullable=False)
    preference_value_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)

