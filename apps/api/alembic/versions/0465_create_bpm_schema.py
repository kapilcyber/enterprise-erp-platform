"""Create bpm schema."""

from collections.abc import Sequence

from alembic import op

revision: str = "0465_create_bpm_schema"
down_revision: str | None = "0464_seed_vp_workflows"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS bpm")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS bpm CASCADE")
