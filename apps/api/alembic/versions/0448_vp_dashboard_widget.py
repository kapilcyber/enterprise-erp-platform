"""Create vp_dashboard_widget per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.dashboard_widget import VpDashboardWidget

revision: str = "0448_vp_dashboard_widget"
down_revision: str | None = "0447_vp_dashboard"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpDashboardWidget.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpDashboardWidget.__table__.drop(bind=op.get_bind(), checkfirst=True)
