"""Create vp_asn per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.asn import VpAsn

revision: str = "0454_vp_asn"
down_revision: str | None = "0453_vp_delivery_schedule"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpAsn.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpAsn.__table__.drop(bind=op.get_bind(), checkfirst=True)
