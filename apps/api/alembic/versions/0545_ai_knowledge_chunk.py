"""Create ai_knowledge_chunk per ERD-27 Phase 2."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.knowledge_chunk import AiKnowledgeChunk  # noqa: E402

revision: str = "0545_ai_knowledge_chunk"
down_revision: str | None = "0544_ai_knowledge_source"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiKnowledgeChunk.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiKnowledgeChunk.__table__.drop(bind=op.get_bind(), checkfirst=True)
