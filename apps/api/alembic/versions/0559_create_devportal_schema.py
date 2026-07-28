"""Create devportal schema — Sprint 28 Phase 0 (no business tables)."""

from collections.abc import Sequence

from alembic import op

revision: str = "0559_create_devportal_schema"
down_revision: str | None = "0558_seed_ai_phase4_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS devportal")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS devportal CASCADE")
