"""Create bpm_notification_template per ERD-25 Phase 3B."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.bpm.models.notification_template import BpmNotificationTemplate

revision: str = "0484_bpm_notification_template"
down_revision: str | None = "0483_bpm_workflow_trigger"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    BpmNotificationTemplate.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    BpmNotificationTemplate.__table__.drop(bind=op.get_bind(), checkfirst=True)
