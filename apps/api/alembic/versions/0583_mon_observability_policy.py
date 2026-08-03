"""Create mon_observability_policy per ERD-29 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.observability_policy import MonObservabilityPolicy

revision: str = "0583_mon_observability_policy"
down_revision: str | None = "0582_create_monitoring_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonObservabilityPolicy.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonObservabilityPolicy.__table__.drop(bind=op.get_bind(), checkfirst=True)
