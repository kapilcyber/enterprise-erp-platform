"""Create dp_api_product per ERD-28 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.api_product import DpApiProduct

revision: str = "0567_dp_api_product"
down_revision: str | None = "0566_dp_application"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpApiProduct.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpApiProduct.__table__.drop(bind=op.get_bind(), checkfirst=True)
