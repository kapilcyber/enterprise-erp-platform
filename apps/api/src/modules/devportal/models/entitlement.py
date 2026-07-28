"""dp_entitlement ORM per ERD-28 Phase 2 — metadata only; no runtime enforcement."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import ENTITLEMENT_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in ENTITLEMENT_STATUS_VALUES)


class DpEntitlement(Base, *DevportalRowMixin):
    __tablename__ = "dp_entitlement"
    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "subscription_id",
            "scope_code",
            name="uk_dp_entitlement_scope",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_entitlement_status"),
        Index("ix_dp_entitlement_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_entitlement_subscription", "subscription_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    subscription_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_subscription.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    scope_code: Mapped[str] = mapped_column(String(100), nullable=False)
    scope_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
