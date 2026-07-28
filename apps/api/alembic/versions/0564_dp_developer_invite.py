"""Create dp_developer_invite per ERD-28 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.developer_invite import DpDeveloperInvite

revision: str = "0564_dp_developer_invite"
down_revision: str | None = "0563_dp_developer_membership"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpDeveloperInvite.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpDeveloperInvite.__table__.drop(bind=op.get_bind(), checkfirst=True)
