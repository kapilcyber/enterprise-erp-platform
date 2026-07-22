"""BPM API route handlers — Phase 1 through Phase 5."""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from modules.bpm.dependencies import (
    PaginationParams,
    SortParams,
    extract_update_fields,
    get_db,
    get_pagination,
    get_sort,
    page_payload,
    require_permission,
)
from modules.bpm.schemas import (
    AssignmentRuleCreate,
    AssignmentRuleResponse,
    AssignmentRuleUpdate,
    BpmDashboardSummaryResponse,
    BusinessRuleCreate,
    BusinessRuleResponse,
    BusinessRuleUpdate,
    DecisionTableCreate,
    DecisionTableResponse,
    DecisionTableRowPayload,
    DecisionTableRowsReplace,
    DecisionTableUpdate,
    DesignerNodeCreate,
    DesignerNodeResponse,
    DesignerNodeUpdate,
    DesignerTransitionCreate,
    DesignerTransitionResponse,
    DesignerTransitionUpdate,
    EscalationPolicyCreate,
    EscalationPolicyResponse,
    EscalationPolicyUpdate,
    FormReferenceCreate,
    FormReferenceResponse,
    FormReferenceUpdate,
    GraphValidateRequest,
    NotificationTemplateCreate,
    NotificationTemplateResponse,
    NotificationTemplateUpdate,
    SimulationRunCreate,
    SimulationRunResponse,
    SimulationRunUpdate,
    SimulationValidateRequest,
    SimulationValidateResponse,
    SlaPolicyCreate,
    SlaPolicyResponse,
    SlaPolicyUpdate,
    TaskDelegationCreate,
    TaskDelegationResponse,
    TemplatePopularItem,
    WorkflowCategoryCreate,
    WorkflowCategoryResponse,
    WorkflowCategoryUpdate,
    WorkflowDefinitionCreate,
    WorkflowDefinitionResponse,
    WorkflowDefinitionUpdate,
    WorkflowHistoryAppend,
    WorkflowHistoryResponse,
    WorkflowInstanceCancel,
    WorkflowInstanceCreate,
    WorkflowInstanceFail,
    WorkflowInstanceResponse,
    WorkflowInstanceUpdate,
    WorkflowTaskAssign,
    WorkflowTaskCreate,
    WorkflowTaskReject,
    WorkflowTaskResponse,
    WorkflowTaskUpdate,
    WorkflowTemplateCopy,
    WorkflowTemplateCreate,
    WorkflowTemplateImportPayload,
    WorkflowTemplateResponse,
    WorkflowTemplateUpdate,
    WorkflowTriggerCreate,
    WorkflowTriggerResponse,
    WorkflowTriggerUpdate,
    WorkflowVariableCreate,
    WorkflowVariableResponse,
    WorkflowVariableUpdate,
    WorkflowVersionClone,
    WorkflowVersionCreate,
    WorkflowVersionPublish,
    WorkflowVersionResponse,
    WorkflowVersionRetire,
    WorkflowVersionUpdate,
)
from modules.bpm.service import (
    AssignmentRuleService,
    BpmDashboardService,
    BusinessRuleService,
    DecisionTableService,
    DesignerGraphValidationService,
    DesignerNodeService,
    DesignerTransitionService,
    EscalationPolicyService,
    FormReferenceService,
    NotificationTemplateService,
    PublishValidationService,
    SimulationRunService,
    SlaPolicyService,
    TaskDelegationService,
    TemplateImportExportService,
    VersionComparisonService,
    WorkflowCategoryService,
    WorkflowDefinitionService,
    WorkflowHistoryService,
    WorkflowInstanceService,
    WorkflowTaskService,
    WorkflowTemplateService,
    WorkflowTriggerService,
    WorkflowVariableService,
    WorkflowVersionService,
)
from modules.foundation.domain.value_objects import TenantContext
from shared.schemas import APIResponse

# --- Dashboard ---

dashboard_router = APIRouter(prefix="/dashboard", tags=["BPM — Dashboard"])


@dashboard_router.get("/summary", response_model=APIResponse[BpmDashboardSummaryResponse])
def dashboard_summary(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.dashboard:read"))],
    db: Annotated[Session, Depends(get_db)],
    company_id: UUID | None = None,
):
    data = BpmDashboardService(db).summary(ctx, company_id=company_id).to_dict()
    return APIResponse(message="OK", data=BpmDashboardSummaryResponse(**data))


# --- Categories ---

categories_router = APIRouter(prefix="/categories", tags=["BPM — Category"])


@categories_router.get("", response_model=APIResponse[dict[str, Any]])
def list_categories(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.category:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    sort: Annotated[SortParams, Depends(get_sort)],
    company_id: UUID | None = None,
    status: str | None = None,
    search: str | None = None,
):
    page = WorkflowCategoryService(db).list(
        ctx,
        company_id=company_id,
        status=status,
        search=search,
        page=pagination.page,
        page_size=pagination.page_size,
        sort_by=sort.sort_by or "sort_order",
        sort_dir=sort.sort_dir,
    )
    return APIResponse(message="OK", data=page_payload(page))


@categories_router.get("/{row_id}", response_model=APIResponse[WorkflowCategoryResponse])
def get_category(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.category:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=WorkflowCategoryService(db).get(ctx, row_id))


@categories_router.post("", response_model=APIResponse[WorkflowCategoryResponse])
def create_category(
    body: WorkflowCategoryCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.category:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=WorkflowCategoryService(db).create(ctx, **body.model_dump(exclude_none=True)),
    )


@categories_router.patch("/{row_id}", response_model=APIResponse[WorkflowCategoryResponse])
def update_category(
    row_id: UUID,
    body: WorkflowCategoryUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.category:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=WorkflowCategoryService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@categories_router.post("/{row_id}/archive", response_model=APIResponse[WorkflowCategoryResponse])
def archive_category(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.category:archive"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Archived", data=WorkflowCategoryService(db).archive(ctx, row_id))


@categories_router.post("/{row_id}/restore", response_model=APIResponse[WorkflowCategoryResponse])
def restore_category(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.category:restore"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Restored", data=WorkflowCategoryService(db).restore(ctx, row_id))


@categories_router.delete("/{row_id}", response_model=APIResponse[WorkflowCategoryResponse])
def delete_category(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.category:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Archived", data=WorkflowCategoryService(db).archive(ctx, row_id)
    )


# --- Templates ---

templates_router = APIRouter(prefix="/templates", tags=["BPM — Template"])


@templates_router.get("", response_model=APIResponse[dict[str, Any]])
def list_templates(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    sort: Annotated[SortParams, Depends(get_sort)],
    company_id: UUID | None = None,
    status: str | None = None,
    category_id: UUID | None = None,
    search: str | None = None,
):
    page = WorkflowTemplateService(db).list(
        ctx,
        company_id=company_id,
        status=status,
        category_id=category_id,
        search=search,
        page=pagination.page,
        page_size=pagination.page_size,
        sort_by=sort.sort_by or "template_name",
        sort_dir=sort.sort_dir,
    )
    return APIResponse(message="OK", data=page_payload(page))


@templates_router.get("/autocomplete", response_model=APIResponse[list[WorkflowTemplateResponse]])
def autocomplete_templates(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:read"))],
    db: Annotated[Session, Depends(get_db)],
    q: Annotated[str, Query(min_length=1)],
    company_id: UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    items = WorkflowTemplateService(db).autocomplete(ctx, q, company_id=company_id, limit=limit)
    return APIResponse(message="OK", data=items)


@templates_router.get("/recent", response_model=APIResponse[list[WorkflowTemplateResponse]])
def recent_templates(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:read"))],
    db: Annotated[Session, Depends(get_db)],
    company_id: UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    items = WorkflowTemplateService(db).recent(ctx, company_id=company_id, limit=limit)
    return APIResponse(message="OK", data=items)


@templates_router.get("/popular", response_model=APIResponse[list[TemplatePopularItem]])
def popular_templates(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:read"))],
    db: Annotated[Session, Depends(get_db)],
    company_id: UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    rows = WorkflowTemplateService(db).popular(ctx, company_id=company_id, limit=limit)
    data = [
        TemplatePopularItem(
            template=WorkflowTemplateResponse.model_validate(r["template"]),
            usage_count=r["usage_count"],
        )
        for r in rows
    ]
    return APIResponse(message="OK", data=data)


@templates_router.post("/import/validate", response_model=APIResponse[dict[str, Any]])
def validate_template_import(
    body: WorkflowTemplateImportPayload,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:import"))],
    db: Annotated[Session, Depends(get_db)],
):
    result = TemplateImportExportService(db).validate_import(
        ctx, body.payload, company_id=body.company_id
    )
    return APIResponse(message="OK", data=result.to_dict())


@templates_router.get("/{row_id}", response_model=APIResponse[WorkflowTemplateResponse])
def get_template(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=WorkflowTemplateService(db).get(ctx, row_id))


@templates_router.get("/{row_id}/export", response_model=APIResponse[dict[str, Any]])
def export_template(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:export"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK", data=TemplateImportExportService(db).export_json(ctx, row_id)
    )


@templates_router.post("", response_model=APIResponse[WorkflowTemplateResponse])
def create_template(
    body: WorkflowTemplateCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=WorkflowTemplateService(db).create(ctx, **body.model_dump(exclude_none=True)),
    )


@templates_router.patch("/{row_id}", response_model=APIResponse[WorkflowTemplateResponse])
def update_template(
    row_id: UUID,
    body: WorkflowTemplateUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=WorkflowTemplateService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@templates_router.post("/{row_id}/copy", response_model=APIResponse[WorkflowTemplateResponse])
def copy_template(
    row_id: UUID,
    body: WorkflowTemplateCopy,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:copy"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Copied",
        data=WorkflowTemplateService(db).copy_template(
            ctx, row_id, template_name=body.template_name
        ),
    )


@templates_router.post("/{row_id}/archive", response_model=APIResponse[WorkflowTemplateResponse])
def archive_template(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:archive"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Archived", data=WorkflowTemplateService(db).archive(ctx, row_id))


@templates_router.post("/{row_id}/restore", response_model=APIResponse[WorkflowTemplateResponse])
def restore_template(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.template:restore"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Restored", data=WorkflowTemplateService(db).restore(ctx, row_id))


# --- Definitions ---

definitions_router = APIRouter(prefix="/definitions", tags=["BPM — Definition"])


@definitions_router.get("", response_model=APIResponse[dict[str, Any]])
def list_definitions(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.definition:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    sort: Annotated[SortParams, Depends(get_sort)],
    company_id: UUID | None = None,
    status: str | None = None,
    module_code: str | None = None,
    entity_type: str | None = None,
    search: str | None = None,
):
    page = WorkflowDefinitionService(db).list(
        ctx,
        company_id=company_id,
        status=status,
        module_code=module_code,
        entity_type=entity_type,
        search=search,
        page=pagination.page,
        page_size=pagination.page_size,
        sort_by=sort.sort_by or "definition_name",
        sort_dir=sort.sort_dir,
    )
    return APIResponse(message="OK", data=page_payload(page))


@definitions_router.get("/{row_id}", response_model=APIResponse[WorkflowDefinitionResponse])
def get_definition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.definition:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=WorkflowDefinitionService(db).get(ctx, row_id))


@definitions_router.post("", response_model=APIResponse[WorkflowDefinitionResponse])
def create_definition(
    body: WorkflowDefinitionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.definition:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=WorkflowDefinitionService(db).create(ctx, **body.model_dump(exclude_none=True)),
    )


@definitions_router.patch("/{row_id}", response_model=APIResponse[WorkflowDefinitionResponse])
def update_definition(
    row_id: UUID,
    body: WorkflowDefinitionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.definition:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=WorkflowDefinitionService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@definitions_router.post(
    "/{row_id}/archive", response_model=APIResponse[WorkflowDefinitionResponse]
)
def archive_definition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.definition:archive"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Archived", data=WorkflowDefinitionService(db).archive(ctx, row_id)
    )


@definitions_router.post(
    "/{row_id}/restore", response_model=APIResponse[WorkflowDefinitionResponse]
)
def restore_definition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.definition:restore"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Restored", data=WorkflowDefinitionService(db).restore(ctx, row_id)
    )


@definitions_router.get(
    "/{row_id}/versions",
    response_model=APIResponse[list[WorkflowVersionResponse]],
)
def list_definition_versions(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.version:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
):
    items = WorkflowVersionService(db).list_by_definition(ctx, row_id)
    start = pagination.offset
    end = start + pagination.page_size
    return APIResponse(message="OK", data=items[start:end])


# --- Versions ---

versions_router = APIRouter(prefix="/versions", tags=["BPM — Version"])


@versions_router.get("/compare", response_model=APIResponse[dict[str, Any]])
def compare_versions(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.version:compare"))],
    db: Annotated[Session, Depends(get_db)],
    left_id: UUID,
    right_id: UUID,
):
    result = VersionComparisonService(db).compare(ctx, left_id, right_id)
    return APIResponse(message="OK", data=result.to_dict())


@versions_router.get("/{row_id}", response_model=APIResponse[WorkflowVersionResponse])
def get_version(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.version:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=WorkflowVersionService(db).get(ctx, row_id))


@versions_router.post("", response_model=APIResponse[WorkflowVersionResponse])
def create_version_draft(
    body: WorkflowVersionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.version:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    definition_id = data.pop("definition_id")
    return APIResponse(
        message="Created",
        data=WorkflowVersionService(db).create_draft(ctx, definition_id, **data),
    )


@versions_router.patch("/{row_id}", response_model=APIResponse[WorkflowVersionResponse])
def update_version(
    row_id: UUID,
    body: WorkflowVersionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.version:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=WorkflowVersionService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@versions_router.post("/{row_id}/validate-publish", response_model=APIResponse[dict[str, Any]])
def validate_publish(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.version:validate"))],
    db: Annotated[Session, Depends(get_db)],
):
    result = PublishValidationService(db).validate(ctx, row_id)
    return APIResponse(message="OK", data=result.to_dict())


@versions_router.post("/{row_id}/publish", response_model=APIResponse[WorkflowVersionResponse])
def publish_version(
    row_id: UUID,
    body: WorkflowVersionPublish,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.version:publish"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Published",
        data=WorkflowVersionService(db).publish(
            ctx, row_id, publish_reason=body.publish_reason
        ),
    )


@versions_router.post("/{row_id}/retire", response_model=APIResponse[WorkflowVersionResponse])
def retire_version(
    row_id: UUID,
    body: WorkflowVersionRetire,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.version:retire"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Retired",
        data=WorkflowVersionService(db).retire(ctx, row_id, retire_reason=body.retire_reason),
    )


@versions_router.post("/{row_id}/clone", response_model=APIResponse[WorkflowVersionResponse])
def clone_version(
    row_id: UUID,
    body: WorkflowVersionClone,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.version:clone"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Cloned",
        data=WorkflowVersionService(db).clone_version(
            ctx,
            row_id,
            version_label=body.version_label,
            change_notes=body.change_notes,
            clone_reason=body.clone_reason,
        ),
    )


# --- Designer Nodes (Phase 2A) ---

nodes_router = APIRouter(prefix="/nodes", tags=["BPM — Designer Node"])


@nodes_router.get("", response_model=APIResponse[list[DesignerNodeResponse]])
def list_nodes(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.node:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK", data=DesignerNodeService(db).list_by_version(ctx, version_id)
    )


@nodes_router.get("/{row_id}", response_model=APIResponse[DesignerNodeResponse])
def get_node(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.node:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=DesignerNodeService(db).get(ctx, row_id))


@nodes_router.post("", response_model=APIResponse[DesignerNodeResponse])
def create_node(
    body: DesignerNodeCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.node:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=DesignerNodeService(db).create(ctx, version_id, **data),
    )


@nodes_router.patch("/{row_id}", response_model=APIResponse[DesignerNodeResponse])
def update_node(
    row_id: UUID,
    body: DesignerNodeUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.node:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=DesignerNodeService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@nodes_router.delete("/{row_id}", response_model=APIResponse[DesignerNodeResponse])
def delete_node(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.node:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=DesignerNodeService(db).soft_delete(ctx, row_id)
    )


# --- Designer Transitions (Phase 2A) ---

transitions_router = APIRouter(prefix="/transitions", tags=["BPM — Designer Transition"])


@transitions_router.get("", response_model=APIResponse[list[DesignerTransitionResponse]])
def list_transitions(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.transition:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=DesignerTransitionService(db).list_by_version(ctx, version_id),
    )


@transitions_router.get("/{row_id}", response_model=APIResponse[DesignerTransitionResponse])
def get_transition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.transition:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=DesignerTransitionService(db).get(ctx, row_id))


@transitions_router.post("", response_model=APIResponse[DesignerTransitionResponse])
def create_transition(
    body: DesignerTransitionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.transition:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    from_node_id = data.pop("from_node_id")
    to_node_id = data.pop("to_node_id")
    return APIResponse(
        message="Created",
        data=DesignerTransitionService(db).create(
            ctx,
            version_id,
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            **data,
        ),
    )


@transitions_router.patch("/{row_id}", response_model=APIResponse[DesignerTransitionResponse])
def update_transition(
    row_id: UUID,
    body: DesignerTransitionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.transition:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=DesignerTransitionService(db).update(
            ctx, row_id, **extract_update_fields(body)
        ),
    )


@transitions_router.delete("/{row_id}", response_model=APIResponse[DesignerTransitionResponse])
def delete_transition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.transition:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=DesignerTransitionService(db).soft_delete(ctx, row_id)
    )


# --- Graph validation (Phase 2A) ---

graph_router = APIRouter(prefix="/graph", tags=["BPM — Designer Graph"])


@graph_router.post("/versions/{version_id}/validate", response_model=APIResponse[dict])
def validate_graph(
    version_id: UUID,
    body: GraphValidateRequest,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.graph:validate"))],
    db: Annotated[Session, Depends(get_db)],
):
    result = DesignerGraphValidationService(db).validate(
        ctx, version_id, allow_cycles=body.allow_cycles
    )
    return APIResponse(message="OK", data=result.to_dict())


# --- Decision Tables (Phase 2B) ---

decision_tables_router = APIRouter(prefix="/decision-tables", tags=["BPM — Decision Table"])


@decision_tables_router.get("", response_model=APIResponse[list[DecisionTableResponse]])
def list_decision_tables(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=DecisionTableService(db).list_by_version(ctx, version_id),
    )


@decision_tables_router.get("/{row_id}", response_model=APIResponse[DecisionTableResponse])
def get_decision_table(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=DecisionTableService(db).get(ctx, row_id))


@decision_tables_router.post("", response_model=APIResponse[DecisionTableResponse])
def create_decision_table(
    body: DecisionTableCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=DecisionTableService(db).create(ctx, version_id, **data),
    )


@decision_tables_router.patch("/{row_id}", response_model=APIResponse[DecisionTableResponse])
def update_decision_table(
    row_id: UUID,
    body: DecisionTableUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=DecisionTableService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@decision_tables_router.delete("/{row_id}", response_model=APIResponse[DecisionTableResponse])
def delete_decision_table(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=DecisionTableService(db).soft_delete(ctx, row_id)
    )


@decision_tables_router.post("/{row_id}/enable", response_model=APIResponse[DecisionTableResponse])
def enable_decision_table(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:enable"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Enabled", data=DecisionTableService(db).enable(ctx, row_id))


@decision_tables_router.post("/{row_id}/disable", response_model=APIResponse[DecisionTableResponse])
def disable_decision_table(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:disable"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Disabled", data=DecisionTableService(db).disable(ctx, row_id))


@decision_tables_router.put("/{row_id}/rows", response_model=APIResponse[DecisionTableResponse])
def replace_decision_table_rows(
    row_id: UUID,
    body: DecisionTableRowsReplace,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Rows replaced",
        data=DecisionTableService(db).replace_rows(ctx, row_id, body.rows),
    )


@decision_tables_router.post("/{row_id}/rows", response_model=APIResponse[DecisionTableResponse])
def add_decision_table_row(
    row_id: UUID,
    body: DecisionTableRowPayload,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Row added",
        data=DecisionTableService(db).add_row(ctx, row_id, body.row),
    )


@decision_tables_router.patch(
    "/{row_id}/rows/{decision_row_id}", response_model=APIResponse[DecisionTableResponse]
)
def update_decision_table_row(
    row_id: UUID,
    decision_row_id: str,
    body: DecisionTableRowPayload,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Row updated",
        data=DecisionTableService(db).update_row(ctx, row_id, decision_row_id, body.row),
    )


@decision_tables_router.delete(
    "/{row_id}/rows/{decision_row_id}", response_model=APIResponse[DecisionTableResponse]
)
def remove_decision_table_row(
    row_id: UUID,
    decision_row_id: str,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.decision_table:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Row removed",
        data=DecisionTableService(db).remove_row(ctx, row_id, decision_row_id),
    )


# --- Business Rules (Phase 2B) ---

business_rules_router = APIRouter(prefix="/business-rules", tags=["BPM — Business Rule"])


@business_rules_router.get("", response_model=APIResponse[list[BusinessRuleResponse]])
def list_business_rules(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.business_rule:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=BusinessRuleService(db).list_by_version(ctx, version_id),
    )


@business_rules_router.get("/{row_id}", response_model=APIResponse[BusinessRuleResponse])
def get_business_rule(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.business_rule:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=BusinessRuleService(db).get(ctx, row_id))


@business_rules_router.post("", response_model=APIResponse[BusinessRuleResponse])
def create_business_rule(
    body: BusinessRuleCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.business_rule:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=BusinessRuleService(db).create(ctx, version_id, **data),
    )


@business_rules_router.patch("/{row_id}", response_model=APIResponse[BusinessRuleResponse])
def update_business_rule(
    row_id: UUID,
    body: BusinessRuleUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.business_rule:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=BusinessRuleService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@business_rules_router.delete("/{row_id}", response_model=APIResponse[BusinessRuleResponse])
def delete_business_rule(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.business_rule:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=BusinessRuleService(db).soft_delete(ctx, row_id)
    )


# --- Workflow Variables (Phase 2B) ---

variables_router = APIRouter(prefix="/variables", tags=["BPM — Workflow Variable"])


@variables_router.get("", response_model=APIResponse[list[WorkflowVariableResponse]])
def list_variables(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.variable:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=WorkflowVariableService(db).list_by_version(ctx, version_id),
    )


@variables_router.get("/{row_id}", response_model=APIResponse[WorkflowVariableResponse])
def get_variable(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.variable:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=WorkflowVariableService(db).get(ctx, row_id))


@variables_router.post("", response_model=APIResponse[WorkflowVariableResponse])
def create_variable(
    body: WorkflowVariableCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.variable:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=WorkflowVariableService(db).create(ctx, version_id, **data),
    )


@variables_router.patch("/{row_id}", response_model=APIResponse[WorkflowVariableResponse])
def update_variable(
    row_id: UUID,
    body: WorkflowVariableUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.variable:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=WorkflowVariableService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@variables_router.delete("/{row_id}", response_model=APIResponse[WorkflowVariableResponse])
def delete_variable(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.variable:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=WorkflowVariableService(db).soft_delete(ctx, row_id)
    )


# --- Form References (Phase 2B) ---

form_references_router = APIRouter(prefix="/form-references", tags=["BPM — Form Reference"])


@form_references_router.get("", response_model=APIResponse[list[FormReferenceResponse]])
def list_form_references(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.form_reference:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=FormReferenceService(db).list_by_version(ctx, version_id),
    )


@form_references_router.get("/{row_id}", response_model=APIResponse[FormReferenceResponse])
def get_form_reference(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.form_reference:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=FormReferenceService(db).get(ctx, row_id))


@form_references_router.post("", response_model=APIResponse[FormReferenceResponse])
def create_form_reference(
    body: FormReferenceCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.form_reference:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=FormReferenceService(db).create(ctx, version_id, **data),
    )


@form_references_router.patch("/{row_id}", response_model=APIResponse[FormReferenceResponse])
def update_form_reference(
    row_id: UUID,
    body: FormReferenceUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.form_reference:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=FormReferenceService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@form_references_router.delete("/{row_id}", response_model=APIResponse[FormReferenceResponse])
def delete_form_reference(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.form_reference:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=FormReferenceService(db).soft_delete(ctx, row_id)
    )


# --- Assignment Rules (Phase 3A) ---

assignment_rules_router = APIRouter(prefix="/assignment-rules", tags=["BPM — Assignment Rule"])


@assignment_rules_router.get("", response_model=APIResponse[list[AssignmentRuleResponse]])
def list_assignment_rules(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.assignment_rule:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=AssignmentRuleService(db).list_by_version(ctx, version_id),
    )


@assignment_rules_router.get("/{row_id}", response_model=APIResponse[AssignmentRuleResponse])
def get_assignment_rule(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.assignment_rule:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=AssignmentRuleService(db).get(ctx, row_id))


@assignment_rules_router.post("", response_model=APIResponse[AssignmentRuleResponse])
def create_assignment_rule(
    body: AssignmentRuleCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.assignment_rule:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=AssignmentRuleService(db).create(ctx, version_id, **data),
    )


@assignment_rules_router.patch("/{row_id}", response_model=APIResponse[AssignmentRuleResponse])
def update_assignment_rule(
    row_id: UUID,
    body: AssignmentRuleUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.assignment_rule:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=AssignmentRuleService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@assignment_rules_router.delete("/{row_id}", response_model=APIResponse[AssignmentRuleResponse])
def delete_assignment_rule(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.assignment_rule:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=AssignmentRuleService(db).soft_delete(ctx, row_id)
    )


# --- Escalation Policies (Phase 3A) ---

escalation_policies_router = APIRouter(
    prefix="/escalation-policies", tags=["BPM — Escalation Policy"]
)


@escalation_policies_router.get("", response_model=APIResponse[list[EscalationPolicyResponse]])
def list_escalation_policies(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.escalation_policy:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=EscalationPolicyService(db).list_by_version(ctx, version_id),
    )


@escalation_policies_router.get("/{row_id}", response_model=APIResponse[EscalationPolicyResponse])
def get_escalation_policy(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.escalation_policy:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=EscalationPolicyService(db).get(ctx, row_id))


@escalation_policies_router.post("", response_model=APIResponse[EscalationPolicyResponse])
def create_escalation_policy(
    body: EscalationPolicyCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.escalation_policy:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=EscalationPolicyService(db).create(ctx, version_id, **data),
    )


@escalation_policies_router.patch("/{row_id}", response_model=APIResponse[EscalationPolicyResponse])
def update_escalation_policy(
    row_id: UUID,
    body: EscalationPolicyUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.escalation_policy:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=EscalationPolicyService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@escalation_policies_router.delete(
    "/{row_id}", response_model=APIResponse[EscalationPolicyResponse]
)
def delete_escalation_policy(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.escalation_policy:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=EscalationPolicyService(db).soft_delete(ctx, row_id)
    )


# --- SLA Policies (Phase 3A) ---

sla_policies_router = APIRouter(prefix="/sla-policies", tags=["BPM — SLA Policy"])


@sla_policies_router.get("", response_model=APIResponse[list[SlaPolicyResponse]])
def list_sla_policies(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.sla_policy:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=SlaPolicyService(db).list_by_version(ctx, version_id),
    )


@sla_policies_router.get("/{row_id}", response_model=APIResponse[SlaPolicyResponse])
def get_sla_policy(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.sla_policy:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=SlaPolicyService(db).get(ctx, row_id))


@sla_policies_router.post("", response_model=APIResponse[SlaPolicyResponse])
def create_sla_policy(
    body: SlaPolicyCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.sla_policy:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=SlaPolicyService(db).create(ctx, version_id, **data),
    )


@sla_policies_router.patch("/{row_id}", response_model=APIResponse[SlaPolicyResponse])
def update_sla_policy(
    row_id: UUID,
    body: SlaPolicyUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.sla_policy:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=SlaPolicyService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@sla_policies_router.delete("/{row_id}", response_model=APIResponse[SlaPolicyResponse])
def delete_sla_policy(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.sla_policy:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=SlaPolicyService(db).soft_delete(ctx, row_id)
    )


# --- Workflow Triggers (Phase 3B) ---

triggers_router = APIRouter(prefix="/triggers", tags=["BPM — Workflow Trigger"])


@triggers_router.get("", response_model=APIResponse[list[WorkflowTriggerResponse]])
def list_triggers(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.trigger:read"))],
    db: Annotated[Session, Depends(get_db)],
    definition_id: UUID | None = None,
    version_id: UUID | None = None,
):
    svc = WorkflowTriggerService(db)
    if version_id is not None:
        data = svc.list_by_version(ctx, version_id)
    elif definition_id is not None:
        data = svc.list_by_definition(ctx, definition_id)
    else:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400, detail="definition_id or version_id query param required"
        )
    return APIResponse(message="OK", data=data)


@triggers_router.get("/{row_id}", response_model=APIResponse[WorkflowTriggerResponse])
def get_trigger(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.trigger:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=WorkflowTriggerService(db).get(ctx, row_id))


@triggers_router.post("", response_model=APIResponse[WorkflowTriggerResponse])
def create_trigger(
    body: WorkflowTriggerCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.trigger:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    definition_id = data.pop("definition_id")
    version_id = data.pop("version_id", None)
    return APIResponse(
        message="Created",
        data=WorkflowTriggerService(db).create(
            ctx, definition_id, version_id=version_id, **data
        ),
    )


@triggers_router.patch("/{row_id}", response_model=APIResponse[WorkflowTriggerResponse])
def update_trigger(
    row_id: UUID,
    body: WorkflowTriggerUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.trigger:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=WorkflowTriggerService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@triggers_router.delete("/{row_id}", response_model=APIResponse[WorkflowTriggerResponse])
def delete_trigger(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.trigger:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=WorkflowTriggerService(db).soft_delete(ctx, row_id)
    )


@triggers_router.post("/{row_id}/enable", response_model=APIResponse[WorkflowTriggerResponse])
def enable_trigger(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.trigger:enable"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Enabled", data=WorkflowTriggerService(db).enable(ctx, row_id))


@triggers_router.post("/{row_id}/disable", response_model=APIResponse[WorkflowTriggerResponse])
def disable_trigger(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.trigger:disable"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Disabled", data=WorkflowTriggerService(db).disable(ctx, row_id)
    )


# --- Notification Templates (Phase 3B) ---

notification_templates_router = APIRouter(
    prefix="/notification-templates", tags=["BPM — Notification Template"]
)


@notification_templates_router.get(
    "", response_model=APIResponse[list[NotificationTemplateResponse]]
)
def list_notification_templates(
    ctx: Annotated[
        TenantContext, Depends(require_permission("bpm.notification_template:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=NotificationTemplateService(db).list_by_version(ctx, version_id),
    )


@notification_templates_router.get(
    "/{row_id}", response_model=APIResponse[NotificationTemplateResponse]
)
def get_notification_template(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("bpm.notification_template:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=NotificationTemplateService(db).get(ctx, row_id))


@notification_templates_router.post(
    "", response_model=APIResponse[NotificationTemplateResponse]
)
def create_notification_template(
    body: NotificationTemplateCreate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("bpm.notification_template:create"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=NotificationTemplateService(db).create(ctx, version_id, **data),
    )


@notification_templates_router.patch(
    "/{row_id}", response_model=APIResponse[NotificationTemplateResponse]
)
def update_notification_template(
    row_id: UUID,
    body: NotificationTemplateUpdate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("bpm.notification_template:update"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=NotificationTemplateService(db).update(
            ctx, row_id, **extract_update_fields(body)
        ),
    )


@notification_templates_router.delete(
    "/{row_id}", response_model=APIResponse[NotificationTemplateResponse]
)
def delete_notification_template(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("bpm.notification_template:delete"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted",
        data=NotificationTemplateService(db).soft_delete(ctx, row_id),
    )


@notification_templates_router.post(
    "/{row_id}/enable", response_model=APIResponse[NotificationTemplateResponse]
)
def enable_notification_template(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("bpm.notification_template:enable"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Enabled", data=NotificationTemplateService(db).enable(ctx, row_id)
    )


@notification_templates_router.post(
    "/{row_id}/disable", response_model=APIResponse[NotificationTemplateResponse]
)
def disable_notification_template(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("bpm.notification_template:disable"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Disabled", data=NotificationTemplateService(db).disable(ctx, row_id)
    )


# --- Workflow Instances (Phase 4) ---

instances_router = APIRouter(prefix="/instances", tags=["BPM — Workflow Instance"])


@instances_router.get("", response_model=APIResponse[list[WorkflowInstanceResponse]])
def list_instances(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID | None = None,
    module_code: str | None = None,
    entity_id: UUID | None = None,
):
    svc = WorkflowInstanceService(db)
    if module_code and entity_id:
        data = svc.list_by_business_entity(ctx, module_code, entity_id)
    elif version_id:
        data = svc.list_by_version(ctx, version_id)
    else:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400,
            detail="version_id or (module_code + entity_id) query params required",
        )
    return APIResponse(message="OK", data=data)


@instances_router.get("/{row_id}", response_model=APIResponse[WorkflowInstanceResponse])
def get_instance(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=WorkflowInstanceService(db).get(ctx, row_id))


@instances_router.post("", response_model=APIResponse[WorkflowInstanceResponse])
def create_instance(
    body: WorkflowInstanceCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=WorkflowInstanceService(db).create(ctx, version_id, **data),
    )


@instances_router.patch("/{row_id}", response_model=APIResponse[WorkflowInstanceResponse])
def update_instance(
    row_id: UUID,
    body: WorkflowInstanceUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=WorkflowInstanceService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@instances_router.delete("/{row_id}", response_model=APIResponse[WorkflowInstanceResponse])
def delete_instance(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=WorkflowInstanceService(db).soft_delete(ctx, row_id)
    )


@instances_router.post("/{row_id}/start", response_model=APIResponse[WorkflowInstanceResponse])
def start_instance(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:start"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Started", data=WorkflowInstanceService(db).start(ctx, row_id))


@instances_router.post("/{row_id}/cancel", response_model=APIResponse[WorkflowInstanceResponse])
def cancel_instance(
    row_id: UUID,
    body: WorkflowInstanceCancel,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:cancel"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Cancelled",
        data=WorkflowInstanceService(db).cancel(ctx, row_id, reason=body.reason),
    )


@instances_router.post("/{row_id}/suspend", response_model=APIResponse[WorkflowInstanceResponse])
def suspend_instance(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:suspend"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Suspended", data=WorkflowInstanceService(db).suspend(ctx, row_id)
    )


@instances_router.post("/{row_id}/resume", response_model=APIResponse[WorkflowInstanceResponse])
def resume_instance(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:resume"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Resumed", data=WorkflowInstanceService(db).resume(ctx, row_id))


@instances_router.post("/{row_id}/complete", response_model=APIResponse[WorkflowInstanceResponse])
def complete_instance(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:complete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Completed", data=WorkflowInstanceService(db).complete(ctx, row_id)
    )


@instances_router.post("/{row_id}/fail", response_model=APIResponse[WorkflowInstanceResponse])
def fail_instance(
    row_id: UUID,
    body: WorkflowInstanceFail,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.instance:fail"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Failed",
        data=WorkflowInstanceService(db).fail(ctx, row_id, reason=body.reason),
    )


# --- Workflow Tasks (Phase 4) ---

tasks_router = APIRouter(prefix="/tasks", tags=["BPM — Workflow Task"])


@tasks_router.get("", response_model=APIResponse[list[WorkflowTaskResponse]])
def list_tasks(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.task:read"))],
    db: Annotated[Session, Depends(get_db)],
    instance_id: UUID,
):
    return APIResponse(
        message="OK", data=WorkflowTaskService(db).list_by_instance(ctx, instance_id)
    )


@tasks_router.get("/{row_id}", response_model=APIResponse[WorkflowTaskResponse])
def get_task(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.task:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=WorkflowTaskService(db).get(ctx, row_id))


@tasks_router.post("", response_model=APIResponse[WorkflowTaskResponse])
def create_task(
    body: WorkflowTaskCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.task:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    instance_id = data.pop("instance_id")
    task_name = data.pop("task_name")
    return APIResponse(
        message="Created",
        data=WorkflowTaskService(db).create(ctx, instance_id, task_name=task_name, **data),
    )


@tasks_router.patch("/{row_id}", response_model=APIResponse[WorkflowTaskResponse])
def update_task(
    row_id: UUID,
    body: WorkflowTaskUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.task:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=WorkflowTaskService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@tasks_router.delete("/{row_id}", response_model=APIResponse[WorkflowTaskResponse])
def delete_task(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.task:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=WorkflowTaskService(db).soft_delete(ctx, row_id)
    )


@tasks_router.post("/{row_id}/assign", response_model=APIResponse[WorkflowTaskResponse])
def assign_task(
    row_id: UUID,
    body: WorkflowTaskAssign,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.task:assign"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Assigned",
        data=WorkflowTaskService(db).assign(ctx, row_id, body.assignee_id),
    )


@tasks_router.post("/{row_id}/claim", response_model=APIResponse[WorkflowTaskResponse])
def claim_task(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.task:claim"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Claimed", data=WorkflowTaskService(db).claim(ctx, row_id))


@tasks_router.post("/{row_id}/release", response_model=APIResponse[WorkflowTaskResponse])
def release_task(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.task:release"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Released", data=WorkflowTaskService(db).release(ctx, row_id))


@tasks_router.post("/{row_id}/complete", response_model=APIResponse[WorkflowTaskResponse])
def complete_task(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.task:complete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Completed", data=WorkflowTaskService(db).complete(ctx, row_id))


@tasks_router.post("/{row_id}/reject", response_model=APIResponse[WorkflowTaskResponse])
def reject_task(
    row_id: UUID,
    body: WorkflowTaskReject,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.task:reject"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Rejected",
        data=WorkflowTaskService(db).reject(ctx, row_id, reason=body.reason),
    )


# --- Workflow History (Phase 4) ---

history_router = APIRouter(prefix="/history", tags=["BPM — Workflow History"])


@history_router.get("", response_model=APIResponse[list[WorkflowHistoryResponse]])
def list_history(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.history:read"))],
    db: Annotated[Session, Depends(get_db)],
    instance_id: UUID | None = None,
    task_id: UUID | None = None,
):
    svc = WorkflowHistoryService(db)
    if task_id is not None:
        data = svc.list_by_task(ctx, task_id)
    elif instance_id is not None:
        data = svc.list_by_instance(ctx, instance_id)
    else:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400, detail="instance_id or task_id query param required"
        )
    return APIResponse(message="OK", data=data)


@history_router.get("/{row_id}", response_model=APIResponse[WorkflowHistoryResponse])
def get_history(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.history:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=WorkflowHistoryService(db).get(ctx, row_id))


@history_router.post("", response_model=APIResponse[WorkflowHistoryResponse])
def append_history(
    body: WorkflowHistoryAppend,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.history:append"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    instance_id = data.pop("instance_id")
    instance = WorkflowInstanceService(db).get(ctx, instance_id)
    return APIResponse(
        message="Appended",
        data=WorkflowHistoryService(db).append(
            ctx, instance_id, company_id=instance.company_id, **data
        ),
    )


# --- Task Delegations (Phase 4) ---

delegations_router = APIRouter(prefix="/delegations", tags=["BPM — Task Delegation"])


@delegations_router.get("", response_model=APIResponse[list[TaskDelegationResponse]])
def list_delegations(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.delegation:read"))],
    db: Annotated[Session, Depends(get_db)],
    task_id: UUID,
):
    return APIResponse(
        message="OK", data=TaskDelegationService(db).list_by_task(ctx, task_id)
    )


@delegations_router.get("/{row_id}", response_model=APIResponse[TaskDelegationResponse])
def get_delegation(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.delegation:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=TaskDelegationService(db).get(ctx, row_id))


@delegations_router.post("", response_model=APIResponse[TaskDelegationResponse])
def create_delegation(
    body: TaskDelegationCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.delegation:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    task_id = data.pop("task_id")
    return APIResponse(
        message="Created",
        data=TaskDelegationService(db).create(ctx, task_id, **data),
    )


@delegations_router.post("/{row_id}/accept", response_model=APIResponse[TaskDelegationResponse])
def accept_delegation(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.delegation:accept"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Accepted", data=TaskDelegationService(db).accept(ctx, row_id)
    )


@delegations_router.post("/{row_id}/reject", response_model=APIResponse[TaskDelegationResponse])
def reject_delegation(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.delegation:reject"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Rejected", data=TaskDelegationService(db).reject(ctx, row_id)
    )


@delegations_router.post("/{row_id}/expire", response_model=APIResponse[TaskDelegationResponse])
def expire_delegation(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.delegation:expire"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Expired", data=TaskDelegationService(db).expire(ctx, row_id)
    )


@delegations_router.delete("/{row_id}", response_model=APIResponse[TaskDelegationResponse])
def delete_delegation(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.delegation:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=TaskDelegationService(db).soft_delete(ctx, row_id)
    )


# --- Simulation Runs (Phase 5) ---

simulations_router = APIRouter(prefix="/simulations", tags=["BPM — Simulation Run"])


@simulations_router.get("", response_model=APIResponse[list[SimulationRunResponse]])
def list_simulations(
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.simulation:read"))],
    db: Annotated[Session, Depends(get_db)],
    version_id: UUID,
):
    return APIResponse(
        message="OK", data=SimulationRunService(db).list_by_version(ctx, version_id)
    )


@simulations_router.post(
    "/validate", response_model=APIResponse[SimulationValidateResponse]
)
def validate_workflow_simulation(
    body: SimulationValidateRequest,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.simulation:validate"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Validated",
        data=SimulationRunService(db).validate_workflow(ctx, body.version_id),
    )


@simulations_router.get("/{row_id}", response_model=APIResponse[SimulationRunResponse])
def get_simulation(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.simulation:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=SimulationRunService(db).get(ctx, row_id))


@simulations_router.post("", response_model=APIResponse[SimulationRunResponse])
def create_simulation(
    body: SimulationRunCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.simulation:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    version_id = data.pop("version_id")
    return APIResponse(
        message="Created",
        data=SimulationRunService(db).create(ctx, version_id, **data),
    )


@simulations_router.patch("/{row_id}", response_model=APIResponse[SimulationRunResponse])
def update_simulation(
    row_id: UUID,
    body: SimulationRunUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.simulation:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=SimulationRunService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@simulations_router.delete("/{row_id}", response_model=APIResponse[SimulationRunResponse])
def delete_simulation(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.simulation:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=SimulationRunService(db).soft_delete(ctx, row_id)
    )


@simulations_router.post("/{row_id}/run", response_model=APIResponse[SimulationRunResponse])
def run_simulation(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.simulation:run"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Simulation complete", data=SimulationRunService(db).run(ctx, row_id)
    )


@simulations_router.post(
    "/{row_id}/cancel", response_model=APIResponse[SimulationRunResponse]
)
def cancel_simulation(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("bpm.simulation:cancel"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Cancelled", data=SimulationRunService(db).cancel(ctx, row_id)
    )


__all__ = [
    "dashboard_router",
    "categories_router",
    "templates_router",
    "definitions_router",
    "versions_router",
    "nodes_router",
    "transitions_router",
    "graph_router",
    "decision_tables_router",
    "business_rules_router",
    "variables_router",
    "form_references_router",
    "assignment_rules_router",
    "escalation_policies_router",
    "sla_policies_router",
    "triggers_router",
    "notification_templates_router",
    "instances_router",
    "tasks_router",
    "history_router",
    "delegations_router",
    "simulations_router",
]

