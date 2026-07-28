"""Create dp_entitlement per ERD-28 Phase 2."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.entitlement import DpEntitlement

revision: str = "0573_dp_entitlement"
down_revision: str | None = "0572_dp_subscription"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpEntitlement.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpEntitlement.__table__.drop(bind=op.get_bind(), checkfirst=True)
