"""Create lc_form_field per ERD-26 Phase 2A."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.form_field import LcFormField  # noqa: E402

revision: str = "0498_lc_form_field"
down_revision: str | None = "0497_lc_form_section"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcFormField.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcFormField.__table__.drop(bind=op.get_bind(), checkfirst=True)
