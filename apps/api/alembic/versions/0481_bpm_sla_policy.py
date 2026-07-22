"""Create bpm_sla_policy per ERD-25 Phase 3A."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from modules.bpm.models.sla_policy import BpmSlaPolicy

revision: str = "0481_bpm_sla_policy"
down_revision: str | None = "0480_bpm_escalation_policy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    BpmSlaPolicy.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    BpmSlaPolicy.__table__.drop(bind=op.get_bind(), checkfirst=True)
