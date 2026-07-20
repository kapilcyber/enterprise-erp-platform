"""Create vendor_portal schema per ERD_24."""

from collections.abc import Sequence

from alembic import op

revision: str = "0443_create_vendor_portal_schema"
down_revision: str | None = "0442_seed_portal_workflows"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS vendor_portal")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS vendor_portal CASCADE")
