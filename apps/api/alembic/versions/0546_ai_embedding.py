"""Create ai_embedding per ERD-27 Phase 2."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.embedding import AiEmbedding  # noqa: E402

revision: str = "0546_ai_embedding"
down_revision: str | None = "0545_ai_knowledge_chunk"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiEmbedding.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiEmbedding.__table__.drop(bind=op.get_bind(), checkfirst=True)
