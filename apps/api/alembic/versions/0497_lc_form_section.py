"""Create lc_form_section per ERD-26 Phase 2A."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.form_section import LcFormSection  # noqa: E402

revision: str = "0497_lc_form_section"
down_revision: str | None = "0496_seed_lowcode_phase1_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcFormSection.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcFormSection.__table__.drop(bind=op.get_bind(), checkfirst=True)
