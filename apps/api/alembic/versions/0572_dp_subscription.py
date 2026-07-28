"""Create dp_subscription per ERD-28 Phase 2."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.subscription import DpSubscription

revision: str = "0572_dp_subscription"
down_revision: str | None = "0571_dp_plan"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpSubscription.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpSubscription.__table__.drop(bind=op.get_bind(), checkfirst=True)
