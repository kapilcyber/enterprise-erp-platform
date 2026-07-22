"""Create bpm_workflow_trigger per ERD-25 Phase 3B."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.bpm.models.workflow_trigger import BpmWorkflowTrigger

revision: str = "0483_bpm_workflow_trigger"
down_revision: str | None = "0482_seed_bpm_phase3a_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    BpmWorkflowTrigger.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    BpmWorkflowTrigger.__table__.drop(bind=op.get_bind(), checkfirst=True)
