"""Create mon_alert_routing_policy per ERD-29 Phase 2."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.alert_routing_policy import MonAlertRoutingPolicy

revision: str = "0592_mon_alert_routing_policy"
down_revision: str | None = "0591_mon_alert_rule"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonAlertRoutingPolicy.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonAlertRoutingPolicy.__table__.drop(bind=op.get_bind(), checkfirst=True)
