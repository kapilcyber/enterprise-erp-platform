"""Create lowcode schema."""

from collections.abc import Sequence

from alembic import op

revision: str = "0492_create_lowcode_schema"
down_revision: str | None = "0491_seed_bpm_phase5_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS lowcode")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS lowcode CASCADE")
