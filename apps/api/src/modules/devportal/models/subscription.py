"""dp_subscription ORM per ERD-28 Phase 2 — binds Application + Product Version + Plan."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.devportal.domain.enums import SUBSCRIPTION_STATUS_VALUES
from modules.devportal.models.mixins import DevportalRowMixin

_STATUSES = ",".join(f"'{t}'" for t in SUBSCRIPTION_STATUS_VALUES)


class DpSubscription(Base, *DevportalRowMixin):
    __tablename__ = "dp_subscription"
    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "application_id",
            "product_version_id",
            "plan_id",
            name="uk_dp_subscription_binding",
        ),
        CheckConstraint(f"status IN ({_STATUSES})", name="ck_dp_subscription_status"),
        Index("ix_dp_subscription_tenant_co_status", "tenant_id", "company_id", "status"),
        Index("ix_dp_subscription_application", "application_id"),
        Index("ix_dp_subscription_plan", "plan_id"),
        Index("ix_dp_subscription_product_version", "product_version_id"),
        {"schema": "devportal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    subscription_code: Mapped[str] = mapped_column(String(50), nullable=False)
    application_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_application.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    product_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_api_product_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    plan_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devportal.dp_plan.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    workflow_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    # Peer UUID — Foundation workflow; Foundation executes approval
    workflow_instance_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
