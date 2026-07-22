"""bpm_designer_node ORM per ERD-25 Phase 2A."""

from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from modules.bpm.domain.enums import NODE_TYPE_VALUES
from modules.bpm.models.mixins import BpmRowMixin

_NODE_TYPES = ",".join(f"'{t}'" for t in NODE_TYPE_VALUES)


class BpmDesignerNode(Base, *BpmRowMixin):
    __tablename__ = "bpm_designer_node"
    __table_args__ = (
        UniqueConstraint("version_id", "node_code", name="uk_bpm_designer_node_code"),
        CheckConstraint(
            f"node_type IN ({_NODE_TYPES})",
            name="ck_bpm_designer_node_type",
        ),
        CheckConstraint(
            "status IN ('active','inactive')",
            name="ck_bpm_designer_node_status",
        ),
        Index("ix_bpm_designer_node_version", "version_id"),
        Index("ix_bpm_designer_node_version_type", "version_id", "node_type"),
        Index("ix_bpm_designer_node_tenant_co", "tenant_id", "company_id"),
        {"schema": "bpm"},
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    node_code: Mapped[str] = mapped_column(String(50), nullable=False)
    node_name: Mapped[str] = mapped_column(String(255), nullable=False)
    node_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active", index=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    position_x: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    position_y: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bpm.bpm_workflow_version.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Optional config blob for designer metadata (not runtime)
    config_json: Mapped[str | None] = mapped_column(Text, nullable=True)
