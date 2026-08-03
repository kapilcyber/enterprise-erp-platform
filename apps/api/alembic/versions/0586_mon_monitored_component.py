"""Create mon_monitored_component per ERD-29 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.monitored_component import MonMonitoredComponent

revision: str = "0586_mon_monitored_component"
down_revision: str | None = "0585_mon_monitored_service"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonMonitoredComponent.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonMonitoredComponent.__table__.drop(bind=op.get_bind(), checkfirst=True)
