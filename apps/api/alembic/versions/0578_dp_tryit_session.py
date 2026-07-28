"""Create dp_tryit_session per ERD-28 Phase 3."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.tryit_session import DpTryitSession

revision: str = "0578_dp_tryit_session"
down_revision: str | None = "0577_dp_sandbox_environment"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpTryitSession.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpTryitSession.__table__.drop(bind=op.get_bind(), checkfirst=True)
