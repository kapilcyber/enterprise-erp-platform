"""bpm_business_rule ORM per ERD-25 Phase 2B."""

from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import BUSINESS_RULE_TYPE_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_RULE_TYPES = ",".join(f"'{t}'" for t in BUSINESS_RULE_TYPE_VALUES)


class BpmBusinessRule(Base, *BpmRowMixin):
    __tablename__ = "bpm_business_rule"
    __table_args__ = (
        UniqueConstraint("version_id", "rule_code", name="uk_bpm_business_rule_code"),
        CheckConstraint(
            f"rule_type IN ({_RULE_TYPES})",
            name="ck_bpm_business_rule_type",
        ),
        CheckConstraint(
            "status IN ('active','inactive','draft')",
            name="ck_bpm_business_rule_status",
        ),
        Index("ix_bpm_business_rule_version", "version_id"),
        Index("ix_bpm_business_rule_decision_table", "decision_table_id"),
        Index("ix_bpm_business_rule_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    rule_code: Mapped[str] = mapped_column(String(50), nullable=False)
    rule_name: Mapped[str] = mapped_column(String(255), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    expression: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    decision_table_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_decision_table.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
