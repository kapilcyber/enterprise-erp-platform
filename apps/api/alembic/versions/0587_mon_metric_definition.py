"""Create mon_metric_definition per ERD-29 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.metric_definition import MonMetricDefinition

revision: str = "0587_mon_metric_definition"
down_revision: str | None = "0586_mon_monitored_component"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonMetricDefinition.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonMetricDefinition.__table__.drop(bind=op.get_bind(), checkfirst=True)
