"""Create vp_invoice_submission per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.invoice_submission import VpInvoiceSubmission

revision: str = "0455_vp_invoice_submission"
down_revision: str | None = "0454_vp_asn"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpInvoiceSubmission.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpInvoiceSubmission.__table__.drop(bind=op.get_bind(), checkfirst=True)
