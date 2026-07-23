"""Create lc_preview_session per ERD-26 Phase 4."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.preview_session import LcPreviewSession  # noqa: E402

revision: str = "0518_lc_preview_session"
down_revision: str | None = "0517_lc_runtime_submission"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcPreviewSession.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcPreviewSession.__table__.drop(bind=op.get_bind(), checkfirst=True)
