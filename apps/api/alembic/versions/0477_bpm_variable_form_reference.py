"""Create bpm_workflow_variable and bpm_form_reference per ERD-25 Phase 2B."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.bpm.models.form_reference import BpmFormReference
from modules.bpm.models.workflow_variable import BpmWorkflowVariable

revision: str = "0477_bpm_variable_form_reference"
down_revision: str | None = "0476_bpm_business_rule"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    BpmWorkflowVariable.__table__.create(bind=op.get_bind(), checkfirst=True)
    BpmFormReference.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    BpmFormReference.__table__.drop(bind=op.get_bind(), checkfirst=True)
    BpmWorkflowVariable.__table__.drop(bind=op.get_bind(), checkfirst=True)
