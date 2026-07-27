"""Create ai_configuration per ERD-27 Phase 1."""

import sys
from collections.abc import Sequence
from pathlib import Path

from alembic import op

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from modules.ai.models.configuration import AiConfiguration  # noqa: E402

revision: str = "0524_ai_configuration"
down_revision: str | None = "0523_ai_provider_credential_reference"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    AiConfiguration.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    AiConfiguration.__table__.drop(bind=op.get_bind(), checkfirst=True)
