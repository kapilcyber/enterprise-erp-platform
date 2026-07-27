"""Create ai_model per ERD-27 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.ai_model import AiModel  # noqa: E402

revision: str = "0522_ai_model"
down_revision: str | None = "0521_ai_provider"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiModel.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiModel.__table__.drop(bind=op.get_bind(), checkfirst=True)
