"""Create lc_runtime_submission per ERD-26 Phase 4."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.runtime_submission import LcRuntimeSubmission  # noqa: E402

revision: str = "0517_lc_runtime_submission"
down_revision: str | None = "0516_lc_publish_history"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcRuntimeSubmission.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcRuntimeSubmission.__table__.drop(bind=op.get_bind(), checkfirst=True)
