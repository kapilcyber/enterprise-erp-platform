"""Create lc_expression per ERD-26 Phase 2C."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.expression import LcExpression  # noqa: E402

revision: str = "0505_lc_expression"
down_revision: str | None = "0504_lc_data_source"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcExpression.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcExpression.__table__.drop(bind=op.get_bind(), checkfirst=True)
