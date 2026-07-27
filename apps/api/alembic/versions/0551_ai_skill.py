"""Create ai_skill per ERD-27 Phase 3."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.skill import AiSkill  # noqa: E402

revision: str = "0551_ai_skill"
down_revision: str | None = "0550_ai_tool_version"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiSkill.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiSkill.__table__.drop(bind=op.get_bind(), checkfirst=True)
