"""BPM dashboard summary service — Phase 1.5 counts only."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.bpm.domain.enums import VersionStatus
from modules.bpm.domain.value_objects import BpmDashboardSummary
from modules.bpm.repository.workflow_category_repository import WorkflowCategoryRepository
from modules.bpm.repository.workflow_definition_repository import WorkflowDefinitionRepository
from modules.bpm.repository.workflow_template_repository import WorkflowTemplateRepository
from modules.bpm.repository.workflow_version_repository import WorkflowVersionRepository
from modules.bpm.service.bpm_scope_validator import BpmScopeValidator
from modules.foundation.domain.value_objects import TenantContext


class BpmDashboardService:
    def __init__(self, db: Session) -> None:
        self._scope = BpmScopeValidator(db)
        self._categories = WorkflowCategoryRepository(db)
        self._templates = WorkflowTemplateRepository(db)
        self._definitions = WorkflowDefinitionRepository(db)
        self._versions = WorkflowVersionRepository(db)

    def summary(
        self, ctx: TenantContext, company_id: UUID | None = None
    ) -> BpmDashboardSummary:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return BpmDashboardSummary(
            categories=self._categories.count_active(ctx, cid),
            templates=self._templates.count_active(ctx, cid),
            definitions=self._definitions.count_active(ctx, cid),
            draft_versions=self._versions.count_by_status(
                ctx, cid, VersionStatus.DRAFT.value
            ),
            published_versions=self._versions.count_by_status(
                ctx, cid, VersionStatus.PUBLISHED.value
            ),
            retired_versions=self._versions.count_by_status(
                ctx, cid, VersionStatus.RETIRED.value
            ),
        )
