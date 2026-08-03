"""Create mon_service_platform_assignment per ERD-29 Phase 3."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.service_platform_assignment import MonServicePlatformAssignment

revision: str = "0597_mon_service_platform_assignment"
down_revision: str | None = "0596_mon_external_platform_binding"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonServicePlatformAssignment.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonServicePlatformAssignment.__table__.drop(bind=op.get_bind(), checkfirst=True)
