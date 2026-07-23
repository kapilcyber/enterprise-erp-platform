"""Add lc_form_field.component_version_id FK per ERD-26 Phase 2B."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0502_lc_form_field_component_version_ref"
down_revision: str | None = "0501_lc_component_version"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "lc_form_field",
        sa.Column("component_version_id", postgresql.UUID(as_uuid=True), nullable=True),
        schema="lowcode",
    )
    op.create_index(
        "ix_lc_form_field_component_version",
        "lc_form_field",
        ["component_version_id"],
        schema="lowcode",
    )
    op.create_foreign_key(
        "fk_lc_form_field_component_version",
        "lc_form_field",
        "lc_component_version",
        ["component_version_id"],
        ["id"],
        source_schema="lowcode",
        referent_schema="lowcode",
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_lc_form_field_component_version",
        "lc_form_field",
        schema="lowcode",
        type_="foreignkey",
    )
    op.drop_index(
        "ix_lc_form_field_component_version",
        table_name="lc_form_field",
        schema="lowcode",
    )
    op.drop_column("lc_form_field", "component_version_id", schema="lowcode")
