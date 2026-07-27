"""Create ai_guardrail_policy per ERD-27 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.guardrail_policy import AiGuardrailPolicy  # noqa: E402

revision: str = "0530_ai_guardrail_policy"
down_revision: str | None = "0529_ai_routing_rule"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiGuardrailPolicy.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiGuardrailPolicy.__table__.drop(bind=op.get_bind(), checkfirst=True)
