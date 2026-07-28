"""Create dp_developer_membership per ERD-28 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.developer_membership import DpDeveloperMembership

revision: str = "0563_dp_developer_membership"
down_revision: str | None = "0562_dp_developer_account"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpDeveloperMembership.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpDeveloperMembership.__table__.drop(bind=op.get_bind(), checkfirst=True)
