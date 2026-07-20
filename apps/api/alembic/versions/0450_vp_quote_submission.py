"""Create vp_quote_submission per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.quote_submission import VpQuoteSubmission

revision: str = "0450_vp_quote_submission"
down_revision: str | None = "0449_vp_rfq_view"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpQuoteSubmission.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpQuoteSubmission.__table__.drop(bind=op.get_bind(), checkfirst=True)
