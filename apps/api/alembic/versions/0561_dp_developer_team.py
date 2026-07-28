"""Create dp_developer_team per ERD-28 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.developer_team import DpDeveloperTeam

revision: str = "0561_dp_developer_team"
down_revision: str | None = "0560_dp_developer_organization"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpDeveloperTeam.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpDeveloperTeam.__table__.drop(bind=op.get_bind(), checkfirst=True)
