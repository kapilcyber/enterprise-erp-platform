"""Create bpm_designer_node per ERD-25 Phase 2A."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.bpm.models.designer_node import BpmDesignerNode

revision: str = "0472_bpm_designer_node"
down_revision: str | None = "0471_bpm_phase15_polish"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    BpmDesignerNode.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    BpmDesignerNode.__table__.drop(bind=op.get_bind(), checkfirst=True)
