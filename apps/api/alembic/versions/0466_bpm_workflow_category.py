"""Create bpm_workflow_category per ERD-25 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.bpm.models.workflow_category import BpmWorkflowCategory

revision: str = "0466_bpm_workflow_category"
down_revision: str | None = "0465_create_bpm_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    BpmWorkflowCategory.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    BpmWorkflowCategory.__table__.drop(bind=op.get_bind(), checkfirst=True)
