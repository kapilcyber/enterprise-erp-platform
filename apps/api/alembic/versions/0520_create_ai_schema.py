"""Create ai schema — Sprint 27 Phase 0 (no business tables)."""

from collections.abc import Sequence

from alembic import op

revision: str = "0520_create_ai_schema"
down_revision: str | None = "0519_seed_lowcode_phase4_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS ai")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS ai CASCADE")
