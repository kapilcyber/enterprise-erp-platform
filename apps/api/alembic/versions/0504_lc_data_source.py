"""Create lc_data_source per ERD-26 Phase 2C."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.data_source import LcDataSource  # noqa: E402

revision: str = "0504_lc_data_source"
down_revision: str | None = "0503_seed_lowcode_phase2b_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcDataSource.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcDataSource.__table__.drop(bind=op.get_bind(), checkfirst=True)
