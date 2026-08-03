"""Create mon_dashboard_definition per ERD-29 Phase 3."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.dashboard_definition import MonDashboardDefinition

revision: str = "0595_mon_dashboard_definition"
down_revision: str | None = "0594_mon_sli_definition"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonDashboardDefinition.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonDashboardDefinition.__table__.drop(bind=op.get_bind(), checkfirst=True)
