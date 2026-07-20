"""Create vp_po_acknowledgement per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.po_acknowledgement import VpPoAcknowledgement

revision: str = "0452_vp_po_acknowledgement"
down_revision: str | None = "0451_vp_purchase_order_view"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpPoAcknowledgement.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpPoAcknowledgement.__table__.drop(bind=op.get_bind(), checkfirst=True)
