"""Create vp_payment_status per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.payment_status import VpPaymentStatus

revision: str = "0456_vp_payment_status"
down_revision: str | None = "0455_vp_invoice_submission"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpPaymentStatus.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpPaymentStatus.__table__.drop(bind=op.get_bind(), checkfirst=True)
