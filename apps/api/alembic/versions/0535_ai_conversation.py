"""Create ai_conversation per ERD-27 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.conversation import AiConversation  # noqa: E402

revision: str = "0535_ai_conversation"
down_revision: str | None = "0534_ai_session"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiConversation.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiConversation.__table__.drop(bind=op.get_bind(), checkfirst=True)
