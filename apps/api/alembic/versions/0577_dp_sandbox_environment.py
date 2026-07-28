"""Create dp_sandbox_environment per ERD-28 Phase 3."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.sandbox_environment import DpSandboxEnvironment

revision: str = "0577_dp_sandbox_environment"
down_revision: str | None = "0576_dp_openapi_artifact_reference"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpSandboxEnvironment.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpSandboxEnvironment.__table__.drop(bind=op.get_bind(), checkfirst=True)
