"""Create dp_api_product_environment per ERD-28 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.api_product_environment import DpApiProductEnvironment

revision: str = "0569_dp_api_product_environment"
down_revision: str | None = "0568_dp_api_product_version"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpApiProductEnvironment.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpApiProductEnvironment.__table__.drop(bind=op.get_bind(), checkfirst=True)
