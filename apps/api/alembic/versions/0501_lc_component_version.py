"""Create lc_component_version per ERD-26 Phase 2B."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.lowcode.models.component_version import LcComponentVersion  # noqa: E402

revision: str = "0501_lc_component_version"
down_revision: str | None = "0500_lc_component"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    LcComponentVersion.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    LcComponentVersion.__table__.drop(bind=op.get_bind(), checkfirst=True)
