"""Create vp_delivery_schedule per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.delivery_schedule import VpDeliverySchedule

revision: str = "0453_vp_delivery_schedule"
down_revision: str | None = "0452_vp_po_acknowledgement"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpDeliverySchedule.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpDeliverySchedule.__table__.drop(bind=op.get_bind(), checkfirst=True)
