"""Create dp_api_product_version per ERD-28 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.api_product_version import DpApiProductVersion

revision: str = "0568_dp_api_product_version"
down_revision: str | None = "0567_dp_api_product"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpApiProductVersion.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpApiProductVersion.__table__.drop(bind=op.get_bind(), checkfirst=True)
