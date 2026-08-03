"""Create mon_monitored_service per ERD-29 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.monitored_service import MonMonitoredService

revision: str = "0585_mon_monitored_service"
down_revision: str | None = "0584_mon_observability_policy_version"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonMonitoredService.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonMonitoredService.__table__.drop(bind=op.get_bind(), checkfirst=True)
