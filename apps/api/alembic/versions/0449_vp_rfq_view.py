"""Create vp_rfq_view per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.rfq_view import VpRfqView

revision: str = "0449_vp_rfq_view"
down_revision: str | None = "0448_vp_dashboard_widget"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpRfqView.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpRfqView.__table__.drop(bind=op.get_bind(), checkfirst=True)
