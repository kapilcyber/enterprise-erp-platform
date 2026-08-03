"""Create mon_service_policy_assignment per ERD-29 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.service_policy_assignment import MonServicePolicyAssignment

revision: str = "0589_mon_service_policy_assignment"
down_revision: str | None = "0588_mon_health_check"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonServicePolicyAssignment.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonServicePolicyAssignment.__table__.drop(bind=op.get_bind(), checkfirst=True)
