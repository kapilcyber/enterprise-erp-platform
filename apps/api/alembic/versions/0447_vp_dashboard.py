"""Create vp_dashboard per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.dashboard import VpDashboard

revision: str = "0447_vp_dashboard"
down_revision: str | None = "0446_vp_portal_session"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpDashboard.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpDashboard.__table__.drop(bind=op.get_bind(), checkfirst=True)
