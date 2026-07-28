"""Create dp_openapi_artifact_reference per ERD-28 Phase 3."""

from collections.abc import Sequence

from alembic import op

from modules.devportal.models.openapi_artifact_reference import DpOpenapiArtifactReference

revision: str = "0576_dp_openapi_artifact_reference"
down_revision: str | None = "0575_dp_documentation_entry"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    DpOpenapiArtifactReference.__table__.create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    DpOpenapiArtifactReference.__table__.drop(bind=op.get_bind(), checkfirst=True)
