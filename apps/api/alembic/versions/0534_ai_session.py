"""Create ai_session per ERD-27 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.session import AiSession  # noqa: E402

revision: str = "0534_ai_session"
down_revision: str | None = "0533_ai_assistant"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiSession.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiSession.__table__.drop(bind=op.get_bind(), checkfirst=True)
