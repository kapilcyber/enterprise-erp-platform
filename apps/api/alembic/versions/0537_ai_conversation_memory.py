"""Create ai_conversation_memory per ERD-27 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.conversation_memory import AiConversationMemory  # noqa: E402

revision: str = "0537_ai_conversation_memory"
down_revision: str | None = "0536_ai_conversation_message"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiConversationMemory.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiConversationMemory.__table__.drop(bind=op.get_bind(), checkfirst=True)
