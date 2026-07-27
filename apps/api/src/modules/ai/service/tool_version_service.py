"""ToolVersionService — Phase 3 create_draft / publish / retire / clone."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from modules.ai.domain.enums import AiEntityType, ToolVersionStatus
from modules.ai.domain.value_objects import PageResult
from modules.ai.models.tool_version import AiToolVersion
from modules.ai.repository.tool_repository import ToolRepository
from modules.ai.repository.tool_version_repository import ToolVersionRepository
from modules.ai.service.ai_number_service import AiNumberService
from modules.ai.service.ai_scope_validator import AiScopeValidator
from modules.ai.service.engines import ToolSchemaValidationEngine, ToolVersionEngine
from modules.ai.service.publish_validation_service import PublishValidationService
from modules.foundation.domain.value_objects import TenantContext
from modules.foundation.service.audit_service import AuditService


class ToolVersionService:
    def __init__(self, db: Session) -> None:
        self._repo = ToolVersionRepository(db)
        self._tools = ToolRepository(db)
        self._scope = AiScopeValidator(db)
        self._numbers = AiNumberService(db)
        self._engine = ToolVersionEngine()
        self._schema_engine = ToolSchemaValidationEngine()
        self._audit = AuditService(db)
        self._publish_validator = PublishValidationService(db)

    def list(
        self,
        ctx: TenantContext,
        company_id: UUID | None = None,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "version_number",
        sort_dir: str = "asc",
        tool_id: UUID | None = None,
    ) -> PageResult:
        cid = self._scope.resolve_company_id(ctx, company_id)
        return self._repo.list_rows(
            ctx,
            cid,
            status=status,
            search=search,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            tool_id=tool_id,
        )

    def list_by_tool(self, ctx: TenantContext, tool_id: UUID):
        if self._tools.get(ctx, tool_id) is None:
            raise NotFoundException("Tool not found")
        return self._repo.list_by_tool(ctx, tool_id)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiToolVersion:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("Tool version not found")
        return row

    def create_draft(
        self,
        ctx: TenantContext,
        tool_id: UUID,
        *,
        input_schema_json: str,
        output_schema_json: str | None = None,
        contract_key: str | None = None,
        version_label: str | None = None,
        change_notes: str | None = None,
        company_id: UUID | None = None,
    ):
        tool = self._tools.get(ctx, tool_id)
        if tool is None:
            raise NotFoundException("Tool not found")
        schema_result = self._schema_engine.validate_input_schema(input_schema_json)
        if not schema_result["valid"]:
            raise ConflictException(
                f"Input schema validation failed: {[i['code'] for i in schema_result['issues']]}"
            )
        cid = self._scope.resolve_company_id(ctx, company_id or tool.company_id)
        version_number = self._repo.next_version_number(ctx, tool_id)
        ver_code = self._numbers.generate(
            AiEntityType.TOOL_VERSION, cid, AiToolVersion, "version_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            tool_id=tool_id,
            version_code=ver_code,
            version_number=version_number,
            version_label=version_label or f"v{version_number}",
            change_notes=change_notes,
            input_schema_json=input_schema_json,
            output_schema_json=output_schema_json,
            contract_key=contract_key,
            status=ToolVersionStatus.DRAFT.value,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_tool_version",
            entity_id=row.id,
            operation="create",
            performed_by=ctx.user_id,
        )
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields):
        row = self.get(ctx, row_id)
        self._engine.assert_editable(row)
        if "input_schema_json" in fields and fields["input_schema_json"] is not None:
            schema_result = self._schema_engine.validate_input_schema(
                fields["input_schema_json"]
            )
            if not schema_result["valid"]:
                raise ConflictException(
                    f"Input schema validation failed: {[i['code'] for i in schema_result['issues']]}"
                )
        fields.pop("status", None)
        fields.pop("tool_id", None)
        fields.pop("version_number", None)
        updated = self._repo.update(ctx, row_id, **fields)
        if updated is None:
            raise NotFoundException("Tool version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_tool_version",
            entity_id=updated.id,
            operation="update",
            performed_by=ctx.user_id,
        )
        return updated

    def archive(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.soft_delete(ctx, row_id)
        if row is None:
            raise NotFoundException("Tool version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_tool_version",
            entity_id=row.id,
            operation="archive",
            performed_by=ctx.user_id,
        )
        return row

    def restore(self, ctx: TenantContext, row_id: UUID):
        row = self._repo.restore(ctx, row_id)
        if row is None:
            raise NotFoundException("Archived tool version not found")
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_tool_version",
            entity_id=row.id,
            operation="restore",
            performed_by=ctx.user_id,
        )
        return row

    def validate_publish(self, ctx: TenantContext, row_id: UUID):
        return self._publish_validator.validate_tool_version(ctx, row_id)

    def publish(self, ctx: TenantContext, row_id: UUID, *, publish_reason: str | None = None):
        result = self._publish_validator.validate_tool_version(ctx, row_id)
        if not result.valid:
            raise ConflictException(
                f"Publish validation failed: {[i.code for i in result.issues]}"
            )
        row = self.get(ctx, row_id)
        prior = self._repo.get_published(ctx, row.tool_id)
        if prior is not None and prior.id != row.id:
            self._engine.retire_published(prior, user_id=ctx.user_id)
            self._repo.update(
                ctx,
                prior.id,
                status=prior.status,
                retired_at=prior.retired_at,
                retired_by=prior.retired_by,
                retire_reason="Auto-retired: superseded by publish",
            )
        self._engine.publish(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            published_at=row.published_at,
            published_by=row.published_by,
            publish_reason=publish_reason,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_tool_version",
            entity_id=row_id,
            operation="publish",
            performed_by=ctx.user_id,
            new_value={"publish_reason": publish_reason},
        )
        return updated

    def retire(self, ctx: TenantContext, row_id: UUID, *, retire_reason: str | None = None):
        row = self.get(ctx, row_id)
        self._engine.retire(row, user_id=ctx.user_id)
        updated = self._repo.update(
            ctx,
            row_id,
            status=row.status,
            retired_at=row.retired_at,
            retired_by=row.retired_by,
            retire_reason=retire_reason,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_tool_version",
            entity_id=row_id,
            operation="retire",
            performed_by=ctx.user_id,
            new_value={"retire_reason": retire_reason},
        )
        return updated

    def clone_version(
        self,
        ctx: TenantContext,
        row_id: UUID,
        *,
        version_label: str | None = None,
        change_notes: str | None = None,
        clone_reason: str | None = None,
    ):
        source = self.get(ctx, row_id)
        cid = source.company_id
        version_number = self._repo.next_version_number(ctx, source.tool_id)
        ver_code = self._numbers.generate(
            AiEntityType.TOOL_VERSION, cid, AiToolVersion, "version_code"
        )
        row = self._repo.create(
            ctx,
            company_id=cid,
            tool_id=source.tool_id,
            version_code=ver_code,
            version_number=version_number,
            version_label=version_label or f"v{version_number}",
            change_notes=change_notes or f"Cloned from version {source.version_number}",
            input_schema_json=source.input_schema_json,
            output_schema_json=source.output_schema_json,
            contract_key=source.contract_key,
            status=ToolVersionStatus.DRAFT.value,
            cloned_from_version_id=source.id,
        )
        self._audit.log_entity_change(
            tenant_id=ctx.tenant_id,
            entity_name="ai_tool_version",
            entity_id=row.id,
            operation="clone",
            performed_by=ctx.user_id,
            new_value={"source_id": str(source.id), "clone_reason": clone_reason},
        )
        return row
