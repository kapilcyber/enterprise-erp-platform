"""Create dp_developer_organization per ERD-28 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.developer_organization import DpDeveloperOrganization

revision: str = "0560_dp_developer_organization"
down_revision: str | None = "0559_create_devportal_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpDeveloperOrganization.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpDeveloperOrganization.__table__.drop(bind=op.get_bind(), checkfirst=True)
