"""Create ai_gateway_policy per ERD-27 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.gateway_policy import AiGatewayPolicy  # noqa: E402

revision: str = "0528_ai_gateway_policy"
down_revision: str | None = "0527_ai_prompt_variable"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiGatewayPolicy.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiGatewayPolicy.__table__.drop(bind=op.get_bind(), checkfirst=True)
