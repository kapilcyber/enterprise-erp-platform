"""Create lc_form_category per ERD-26 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.form_category import LcFormCategory  # noqa: E402

revision: str = "0493_lc_form_category"
down_revision: str | None = "0492_create_lowcode_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcFormCategory.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcFormCategory.__table__.drop(bind=op.get_bind(), checkfirst=True)
