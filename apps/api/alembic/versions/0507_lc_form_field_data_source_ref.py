"""Add lc_form_field.data_source_id FK per ERD-26 Phase 2C."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0507_lc_form_field_data_source_ref"
down_revision: str | None = "0506_lc_expression_binding"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "lc_form_field",
        sa.Column("data_source_id", postgresql.UUID(as_uuid=True), nullable=True),
        schema="lowcode",
    )
    op.create_index(
        "ix_lc_form_field_data_source",
        "lc_form_field",
        ["data_source_id"],
        schema="lowcode",
    )
    op.create_foreign_key(
        "fk_lc_form_field_data_source",
        "lc_form_field",
        "lc_data_source",
        ["data_source_id"],
        ["id"],
        source_schema="lowcode",
        referent_schema="lowcode",
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_lc_form_field_data_source",
        "lc_form_field",
        schema="lowcode",
        type_="foreignkey",
    )
    op.drop_index(
        "ix_lc_form_field_data_source",
        table_name="lc_form_field",
        schema="lowcode",
    )
    op.drop_column("lc_form_field", "data_source_id", schema="lowcode")
