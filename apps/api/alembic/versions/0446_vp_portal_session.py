"""Create vp_portal_session per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.portal_session import VpPortalSession

revision: str = "0446_vp_portal_session"
down_revision: str | None = "0445_vp_supplier_profile"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpPortalSession.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpPortalSession.__table__.drop(bind=op.get_bind(), checkfirst=True)
