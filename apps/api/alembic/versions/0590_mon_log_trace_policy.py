"""Create mon_log_trace_policy per ERD-29 Phase 2."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.log_trace_policy import MonLogTracePolicy

revision: str = "0590_mon_log_trace_policy"
down_revision: str | None = "0589_mon_service_policy_assignment"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonLogTracePolicy.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonLogTracePolicy.__table__.drop(bind=op.get_bind(), checkfirst=True)
