"""Create lc_event_handler per ERD-26 Phase 3A."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.event_handler import LcEventHandler  # noqa: E402

revision: str = "0509_lc_event_handler"
down_revision: str | None = "0508_seed_lowcode_phase2c_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcEventHandler.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcEventHandler.__table__.drop(bind=op.get_bind(), checkfirst=True)
