"""Create vp_login_audit per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.login_audit import VpLoginAudit

revision: str = "0461_vp_login_audit"
down_revision: str | None = "0460_vp_preference"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpLoginAudit.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpLoginAudit.__table__.drop(bind=op.get_bind(), checkfirst=True)
