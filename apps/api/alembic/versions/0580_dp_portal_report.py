"""Create dp_portal_report per ERD-28 Phase 4."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.portal_report import DpPortalReport

revision: str = "0580_dp_portal_report"
down_revision: str | None = "0579_seed_devportal_phase3_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpPortalReport.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpPortalReport.__table__.drop(bind=op.get_bind(), checkfirst=True)
