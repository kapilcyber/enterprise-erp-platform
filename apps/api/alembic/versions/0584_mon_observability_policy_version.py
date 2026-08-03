"""Create mon_observability_policy_version per ERD-29 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.observability_policy_version import MonObservabilityPolicyVersion

revision: str = "0584_mon_observability_policy_version"
down_revision: str | None = "0583_mon_observability_policy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonObservabilityPolicyVersion.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonObservabilityPolicyVersion.__table__.drop(bind=op.get_bind(), checkfirst=True)
