"""Create vp_preference per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.preference import VpPreference

revision: str = "0460_vp_preference"
down_revision: str | None = "0459_vp_thread_and_message"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpPreference.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpPreference.__table__.drop(bind=op.get_bind(), checkfirst=True)
