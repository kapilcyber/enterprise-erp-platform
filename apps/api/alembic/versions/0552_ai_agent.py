"""Create ai_agent per ERD-27 Phase 3."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.agent import AiAgent  # noqa: E402

revision: str = "0552_ai_agent"
down_revision: str | None = "0551_ai_skill"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiAgent.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiAgent.__table__.drop(bind=op.get_bind(), checkfirst=True)
