"""Create mon_observability_report per ERD-29 Phase 4."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.observability_report import MonObservabilityReport

revision: str = "0599_mon_observability_report"
down_revision: str | None = "0598_mon_signal_correlation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonObservabilityReport.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonObservabilityReport.__table__.drop(bind=op.get_bind(), checkfirst=True)
