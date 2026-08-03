"""Create mon_health_check per ERD-29 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.health_check import MonHealthCheck

revision: str = "0588_mon_health_check"
down_revision: str | None = "0587_mon_metric_definition"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonHealthCheck.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonHealthCheck.__table__.drop(bind=op.get_bind(), checkfirst=True)
