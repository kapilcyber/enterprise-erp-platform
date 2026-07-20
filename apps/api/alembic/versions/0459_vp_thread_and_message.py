"""Create vp_message_thread and vp_message per ERD_24."""

from collections.abc import Sequence
import sys
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.vendor_portal.models.message_thread import VpMessageThread
from modules.vendor_portal.models.message import VpMessage

revision: str = "0459_vp_thread_and_message"
down_revision: str | None = "0458_vp_notification"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    VpMessageThread.__table__.create(bind=op.get_bind(), checkfirst=True)
    VpMessage.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    VpMessage.__table__.drop(bind=op.get_bind(), checkfirst=True)
    VpMessageThread.__table__.drop(bind=op.get_bind(), checkfirst=True)
