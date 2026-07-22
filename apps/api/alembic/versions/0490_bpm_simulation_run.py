"""Create bpm_simulation_run per ERD-25 Phase 5."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.bpm.models.simulation_run import BpmSimulationRun

revision: str = "0490_bpm_simulation_run"
down_revision: str | None = "0489_seed_bpm_phase4_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    BpmSimulationRun.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    BpmSimulationRun.__table__.drop(bind=op.get_bind(), checkfirst=True)
