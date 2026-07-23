"""Create lc_localization_entry per ERD-26 Phase 3A."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.localization_entry import LcLocalizationEntry  # noqa: E402

revision: str = "0510_lc_localization_entry"
down_revision: str | None = "0509_lc_event_handler"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcLocalizationEntry.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcLocalizationEntry.__table__.drop(bind=op.get_bind(), checkfirst=True)
