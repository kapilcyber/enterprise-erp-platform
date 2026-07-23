"""Create lc_form_version per ERD-26 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.form_version import LcFormVersion  # noqa: E402

revision: str = "0495_lc_form_version"
down_revision: str | None = "0494_lc_form_definition"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcFormVersion.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcFormVersion.__table__.drop(bind=op.get_bind(), checkfirst=True)
