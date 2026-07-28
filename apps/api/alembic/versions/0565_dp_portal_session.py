"""Create dp_portal_session per ERD-28 Phase 1."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.portal_session import DpPortalSession

revision: str = "0565_dp_portal_session"
down_revision: str | None = "0564_dp_developer_invite"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpPortalSession.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpPortalSession.__table__.drop(bind=op.get_bind(), checkfirst=True)
