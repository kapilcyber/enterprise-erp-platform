"""Create bpm_workflow_task per ERD-25 Phase 4."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.bpm.models.workflow_task import BpmWorkflowTask

revision: str = "0487_bpm_workflow_task"
down_revision: str | None = "0486_bpm_workflow_instance"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    BpmWorkflowTask.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    BpmWorkflowTask.__table__.drop(bind=op.get_bind(), checkfirst=True)
