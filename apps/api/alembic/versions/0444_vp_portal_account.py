"""Create vp_portal_account per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.portal_account import VpPortalAccount

revision: str = "0444_vp_portal_account"
down_revision: str | None = "0443_create_vendor_portal_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpPortalAccount.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpPortalAccount.__table__.drop(bind=op.get_bind(), checkfirst=True)
