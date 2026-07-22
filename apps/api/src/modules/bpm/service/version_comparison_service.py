"""Version comparison service — Phase 1.5."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.bpm.domain.value_objects import FieldDiff, VersionComparisonResult
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.foundation.domain.value_objects import TenantContext

_COMPARE_FIELDS = (
    "version_number",
    "version_label",
    "version_code",
    "change_notes",
    "status",
    "publish_reason",
    "retire_reason",
    "clone_reason",
    "cloned_from_version_id",
    "published_at",
    "published_by",
    "retired_at",
    "retired_by",
)


class VersionComparisonService:
    def __init__(self, db: Session) -> None:
        self._repo = WorkflowVersionRepository(db)

    def compare(
        self, ctx: TenantContext, left_id: UUID, right_id: UUID
    ) -> VersionComparisonResult:
        left = self._repo.get(ctx, left_id)
        right = self._repo.get(ctx, right_id)
        if left is None or right is None:
            raise NotFoundException("One or both workflow versions not found")

        diffs: list[FieldDiff] = []
        for name in _COMPARE_FIELDS:
            lv = getattr(left, name, None)
            rv = getattr(right, name, None)
            # Normalize UUID / datetime to string for stable JSON
            lv_n = str(lv) if lv is not None else None
            rv_n = str(rv) if rv is not None else None
            if lv_n != rv_n:
                diffs.append(FieldDiff(field=name, left=lv_n, right=rv_n))

        return VersionComparisonResult(
            left_version_id=left.id,
            right_version_id=right.id,
            same_definition=left.definition_id == right.definition_id,
            differences=diffs,
        )
