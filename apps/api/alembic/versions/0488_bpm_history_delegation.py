"""Create bpm_workflow_history and bpm_task_delegation per ERD-25 Phase 4."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.bpm.models.task_delegation import BpmTaskDelegation
from modules.bpm.models.workflow_history import BpmWorkflowHistory

revision: str = "0488_bpm_history_delegation"
down_revision: str | None = "0487_bpm_workflow_task"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    BpmWorkflowHistory.__table__.create(bind=op.get_bind(), checkfirst=True)
    BpmTaskDelegation.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    BpmTaskDelegation.__table__.drop(bind=op.get_bind(), checkfirst=True)
    BpmWorkflowHistory.__table__.drop(bind=op.get_bind(), checkfirst=True)
