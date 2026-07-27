"""Create ai_usage_record per ERD-27 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.usage_record import AiUsageRecord  # noqa: E402

revision: str = "0539_ai_usage_record"
down_revision: str | None = "0538_ai_context_package"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiUsageRecord.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiUsageRecord.__table__.drop(bind=op.get_bind(), checkfirst=True)
