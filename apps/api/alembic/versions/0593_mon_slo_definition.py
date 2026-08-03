"""Create mon_slo_definition per ERD-29 Phase 3."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.slo_definition import MonSloDefinition

revision: str = "0593_mon_slo_definition"
down_revision: str | None = "0592_mon_alert_routing_policy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonSloDefinition.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonSloDefinition.__table__.drop(bind=op.get_bind(), checkfirst=True)
