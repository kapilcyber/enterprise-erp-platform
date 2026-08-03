"""Create mon_sli_definition per ERD-29 Phase 3."""

from collections.abc import Sequence

from alembic import op

from modules.monitoring.models.sli_definition import MonSliDefinition

revision: str = "0594_mon_sli_definition"
down_revision: str | None = "0593_mon_slo_definition"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    MonSliDefinition.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    MonSliDefinition.__table__.drop(bind=op.get_bind(), checkfirst=True)
