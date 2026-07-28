"""Create dp_plan per ERD-28 Phase 2."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.plan import DpPlan

revision: str = "0571_dp_plan"
down_revision: str | None = "0570_seed_devportal_phase1_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpPlan.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpPlan.__table__.drop(bind=op.get_bind(), checkfirst=True)
