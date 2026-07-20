"""Vendor Portal ORM — vp_message_thread per ERD_24."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.vendor_portal.models.mixins import VpRowMixin


class VpMessageThread(Base, *VpRowMixin):
    __tablename__ = "vp_message_thread"
    __table_args__ = (
        UniqueConstraint("company_id", "thread_number", name="uk_vp_message_thread_thread_number"),
        CheckConstraint(
            "status IN ('open','waiting','closed')",
            name="ck_vp_message_thread_status",
        ),
        Index("ix_vp_message_thread_tenant_co_status", "tenant_id", "company_id", "status"),
        {"schema": "vendor_portal"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    thread_number: Mapped[str] = mapped_column(String(50), nullable=False)
    portal_account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendor_portal.vp_portal_account.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    related_entity_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    related_entity_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    qm_ncr_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    qm_incoming_inspection_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
    )
    helpdesk_ticket_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    service_request_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="open", index=True)

