"""Create dp_application per ERD-28 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.application import DpApplication

revision: str = "0566_dp_application"
down_revision: str | None = "0565_dp_portal_session"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpApplication.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpApplication.__table__.drop(bind=op.get_bind(), checkfirst=True)
