"""Create monitoring schema — Sprint 29 Phase 0 (no business tables)."""

from collections.abc import Sequence

from alembic import op

revision: str = "0582_create_monitoring_schema"
down_revision: str | None = "0581_seed_devportal_phase4_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS monitoring")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS monitoring CASCADE")
