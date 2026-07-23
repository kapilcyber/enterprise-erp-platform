"""Create lc_expression_binding per ERD-26 Phase 2C."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.expression_binding import LcExpressionBinding  # noqa: E402

revision: str = "0506_lc_expression_binding"
down_revision: str | None = "0505_lc_expression"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcExpressionBinding.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcExpressionBinding.__table__.drop(bind=op.get_bind(), checkfirst=True)
