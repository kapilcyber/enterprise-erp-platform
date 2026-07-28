"""Create dp_developer_account per ERD-28 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.developer_account import DpDeveloperAccount

revision: str = "0562_dp_developer_account"
down_revision: str | None = "0561_dp_developer_team"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpDeveloperAccount.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpDeveloperAccount.__table__.drop(bind=op.get_bind(), checkfirst=True)
