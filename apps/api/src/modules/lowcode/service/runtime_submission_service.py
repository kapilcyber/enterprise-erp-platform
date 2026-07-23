"""RuntimeSubmissionService — Phase 4 correlation envelope (no business SoR)."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService
from modules.lowcode.domain.enums import LowcodeEntityType, SubmissionStatus, VersionStatus
from modules.lowcode.domain.exceptions import InvalidRuntimeSubmissionState
from modules.lowcode.models import LcRuntimeSubmission
from modules.lowcode.repository.form_version_repository import FormVersionRepository
from modules.lowcode.repository.page_version_repository import PageVersionRepository
from modules.lowcode.repository.runtime_submission_repository import (
    RuntimeSubmissionRepository,
)
from modules.lowcode.service.engines import RuntimeSubmissionEngine
from modules.lowcode.service.lowcode_number_service import LowcodeNumberService
from modules.lowcode.service.lowcode_scope_validator import LowcodeScopeValidator


class RuntimeSubmissionService:
    def __init__(self, db: Session) -> None:
        self._repo = RuntimeSubmissionRepository(db)
        self._form_versions = FormVersionRepository(db)
        self._page_versions = PageVersionRepository(db)
        self._scope = LowcodeScopeValidator(db)
        self._numbers = LowcodeNumberService(db)
        self._engine = RuntimeSubmissionEngine()
        self._audit = AuditService(db)

    def _require_published_form(self, ctx: TenantContext, form_version_id: UUID | None):
        if form_version_id is None:
            return None
        row = self._form_versions.get(ctx, form_version_id)
        if row is None:
            raise NotFoundException("Form version not found")
        if row.status != VersionStatus.PUBLISHED.value:
            raise InvalidRuntimeSubmissionState(
                "Runtime submission requires a Published form version"
            )
        return row

    def _require_published_page(self, ctx: TenantContext, page_version_id: UUID | None):
        if page_version_id is None:
            return None
        row = self._page_versions.get(ctx, page_version_id)
        if row is None:
            raise NotFoundException("Page version not found")
        if row.status != VersionStatus.PUBLISHED.value:
            raise InvalidRuntimeSubmissionState(
                "Runtime submission requires a Published page version"
            )
        return row

    def get(self, ctx: TenantContext, row_id: UUID) -> LcRuntimeSubmission:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Runtime submission not found")
        return row

    def get_by_correlation(
        self, ctx: TenantContext, correlation_id: str, company_id: UUID | None = None
    ) -> LcRuntimeSubmission:
        cid = self._scope.resolve_company_id(ctx, company_id)
        row = self._repo.get_by_correlation(ctx, cid, correlation_id)
        if row is None:
            raise NotFoundException("Runtime submission not found")
        return row

    def list_by_module_entity(
        self, ctx: TenantContext, module_code: str, entity_id: UUID
    ):
        self._engine.assert_module_context(module_code, entity_id)
        return self._repo.list_by_module_entity(ctx, module_code, entity_id)

    def create(self, ctx: TenantContext, company_id: UUID | None = None, **fields):
        form_version_id = fields.get("form_version_id")
        page_version_id = fields.get("page_version_id")
        self._engine.assert_version_target(
            form_version_id=form_version_id, page_version_id=page_version_id
        )
        form_ver = self._require_published_form(ctx, form_version_id)
        page_ver = self._require_published_page(ctx, page_version_id)
        module_code = fields.get("module_code")
        entity_id = fields.get("entity_id")
        self._engine.assert_module_context(module_code, entity_id)
        correlation_id = fields.get("correlation_id") or str(uuid4())
        self._engine.assert_correlation_id(correlation_id)
        status = fields.get("submission_status") or SubmissionStatus.RECEIVED.value
        self._engine.assert_valid_status(status)

        company = (
            (form_ver.company_id if form_ver else None)
            or (page_ver.company_id if page_ver else None)
            or company_id
        )
        cid = self._scope.resolve_company_id(ctx, company)
        existing = self._repo.get_by_correlation(ctx, cid, correlation_id)
        if existing is not None:
            raise InvalidRuntimeSubmissionState(
                f"correlation_id '{correlation_id}' already exists"
            )
        code = fields.pop("submission_code", None) or self._numbers.generate(
            LowcodeEntityType.RUNTIME_SUBMISSION,
            cid,
            LcRuntimeSubmission,
            "submission_code",
        )
        fields["correlation_id"] = correlation_id
        fields["submission_status"] = status
        row = self._repo.create(
            ctx, company_id=cid, submission_code=code, **fields
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_runtime_submission",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update_status(
        self,
        ctx: TenantContext,
        row_id: UUID,
        *,
        submission_status: str,
        validation_result_json: str | None = None,
        metadata_json: str | None = None,
    ):
        row = self.get(ctx, row_id)
        self._engine.assert_valid_status(submission_status)
        updated = self._repo.update(
            ctx,
            row_id,
            submission_status=submission_status,
            validation_result_json=validation_result_json
            if validation_result_json is not None
            else row.validation_result_json,
            metadata_json=metadata_json if metadata_json is not None else row.metadata_json,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="lc_runtime_submission",
            entity_id=row_id,
            operation="update",
            performed_by=ctx.user_id,
            new_value={"submission_status": submission_status},
        )
        return updated
