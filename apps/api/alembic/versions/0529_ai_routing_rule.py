"""Create ai_routing_rule per ERD-27 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.routing_rule import AiRoutingRule  # noqa: E402

revision: str = "0529_ai_routing_rule"
down_revision: str | None = "0528_ai_gateway_policy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiRoutingRule.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiRoutingRule.__table__.drop(bind=op.get_bind(), checkfirst=True)
