"""Create lc_publish_history per ERD-26 Phase 4."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.publish_history import LcPublishHistory  # noqa: E402

revision: str = "0516_lc_publish_history"
down_revision: str | None = "0515_seed_lowcode_phase3b_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcPublishHistory.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcPublishHistory.__table__.drop(bind=op.get_bind(), checkfirst=True)
