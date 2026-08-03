"""Create mon_alert_rule per ERD-29 Phase 2."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.alert_rule import MonAlertRule

revision: str = "0591_mon_alert_rule"
down_revision: str | None = "0590_mon_log_trace_policy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonAlertRule.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonAlertRule.__table__.drop(bind=op.get_bind(), checkfirst=True)
