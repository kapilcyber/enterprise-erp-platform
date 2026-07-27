"""Create ai_agent_version per ERD-27 Phase 3."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.agent_version import AiAgentVersion  # noqa: E402

revision: str = "0553_ai_agent_version"
down_revision: str | None = "0552_ai_agent"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiAgentVersion.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiAgentVersion.__table__.drop(bind=op.get_bind(), checkfirst=True)
