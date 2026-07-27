"""Create ai_moderation_policy per ERD-27 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.moderation_policy import AiModerationPolicy  # noqa: E402

revision: str = "0531_ai_moderation_policy"
down_revision: str | None = "0530_ai_guardrail_policy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiModerationPolicy.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiModerationPolicy.__table__.drop(bind=op.get_bind(), checkfirst=True)
