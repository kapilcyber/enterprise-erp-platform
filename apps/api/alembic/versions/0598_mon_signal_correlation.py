"""Create mon_signal_correlation per ERD-29 Phase 3."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.signal_correlation import MonSignalCorrelation

revision: str = "0598_mon_signal_correlation"
down_revision: str | None = "0597_mon_service_platform_assignment"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonSignalCorrelation.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonSignalCorrelation.__table__.drop(bind=op.get_bind(), checkfirst=True)
