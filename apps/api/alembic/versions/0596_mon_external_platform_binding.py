"""Create mon_external_platform_binding per ERD-29 Phase 3."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.external_platform_binding import MonExternalPlatformBinding

revision: str = "0596_mon_external_platform_binding"
down_revision: str | None = "0595_mon_dashboard_definition"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonExternalPlatformBinding.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonExternalPlatformBinding.__table__.drop(bind=op.get_bind(), checkfirst=True)
