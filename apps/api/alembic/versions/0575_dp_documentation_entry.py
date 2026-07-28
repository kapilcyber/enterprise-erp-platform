"""Create dp_documentation_entry per ERD-28 Phase 3."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.documentation_entry import DpDocumentationEntry

revision: str = "0575_dp_documentation_entry"
down_revision: str | None = "0574_seed_devportal_phase2_permissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpDocumentationEntry.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpDocumentationEntry.__table__.drop(bind=op.get_bind(), checkfirst=True)
