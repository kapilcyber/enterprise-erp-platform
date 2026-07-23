"""Low-Code API route handlers — Phase 1."""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext
from modules.lowcode.dependencies import (
    PaginationParams,
    SortParams,
    extract_update_fields,
    get_db,
    get_pagination,
    get_sort,
    page_payload,
    require_permission,
)
from modules.lowcode.schemas import (
    ComponentCreate,
    ComponentResponse,
    ComponentUpdate,
    ComponentVersionClone,
    ComponentVersionCreate,
    ComponentVersionPublish,
    ComponentVersionResponse,
    ComponentVersionRetire,
    ComponentVersionUpdate,
    DataSourceCreate,
    DataSourceResponse,
    DataSourceUpdate,
    EventHandlerCreate,
    EventHandlerResponse,
    EventHandlerUpdate,
    ExpressionBindingCreate,
    ExpressionBindingResponse,
    ExpressionBindingUpdate,
    ExpressionCreate,
    ExpressionPublish,
    ExpressionResponse,
    ExpressionRetire,
    ExpressionUpdate,
    FormCategoryCreate,
    FormCategoryResponse,
    FormCategoryUpdate,
    FormDefinitionCreate,
    FormDefinitionResponse,
    FormDefinitionUpdate,
    FormFieldCreate,
    FormFieldResponse,
    FormFieldUpdate,
    FormSectionCreate,
    FormSectionResponse,
    FormSectionUpdate,
    FormVersionClone,
    FormVersionCreate,
    FormVersionPublish,
    FormVersionResponse,
    FormVersionRetire,
    FormVersionUpdate,
    LocalizationEntryCreate,
    LocalizationEntryPublish,
    LocalizationEntryResponse,
    LocalizationEntryRetire,
    LocalizationEntryUpdate,
    PageDefinitionCreate,
    PageDefinitionResponse,
    PageDefinitionUpdate,
    PageRegionCreate,
    PageRegionResponse,
    PageRegionUpdate,
    PageVersionClone,
    PageVersionCreate,
    PageVersionPublish,
    PageVersionResponse,
    PageVersionRetire,
    PageVersionUpdate,
    PreviewSessionCreate,
    PreviewSessionResponse,
    PublishHistoryResponse,
    RuntimeSubmissionCreate,
    RuntimeSubmissionResponse,
    RuntimeSubmissionStatusUpdate,
)
from modules.lowcode.service.component_service import ComponentService
from modules.lowcode.service.component_version_service import ComponentVersionService
from modules.lowcode.service.data_source_service import DataSourceService
from modules.lowcode.service.event_handler_service import EventHandlerService
from modules.lowcode.service.expression_binding_service import ExpressionBindingService
from modules.lowcode.service.expression_service import ExpressionService
from modules.lowcode.service.form_category_service import FormCategoryService
from modules.lowcode.service.form_definition_service import FormDefinitionService
from modules.lowcode.service.form_field_service import FormFieldService
from modules.lowcode.service.form_section_service import FormSectionService
from modules.lowcode.service.form_structure_validation_service import (
    FormStructureValidationService,
)
from modules.lowcode.service.form_version_service import FormVersionService
from modules.lowcode.service.localization_entry_service import LocalizationEntryService
from modules.lowcode.service.page_definition_service import PageDefinitionService
from modules.lowcode.service.page_region_service import PageRegionService
from modules.lowcode.service.page_version_service import PageVersionService
from modules.lowcode.service.preview_session_service import PreviewSessionService
from modules.lowcode.service.publish_history_service import PublishHistoryService
from modules.lowcode.service.publish_validation_service import PublishValidationService
from modules.lowcode.service.runtime_submission_service import RuntimeSubmissionService
from shared.schemas import APIResponse

# --- Categories ---

categories_router = APIRouter(prefix="/categories", tags=["Low-Code — Category"])


@categories_router.get("", response_model=APIResponse[dict[str, Any]])
def list_categories(
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.category:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    sort: Annotated[SortParams, Depends(get_sort)],
    company_id: UUID | None = None,
    status: str | None = None,
    search: str | None = None,
):
    page = FormCategoryService(db).list(
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


@categories_router.get("/{row_id}", response_model=APIResponse[FormCategoryResponse])
def get_category(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.category:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=FormCategoryService(db).get(ctx, row_id))


@categories_router.post("", response_model=APIResponse[FormCategoryResponse])
def create_category(
    body: FormCategoryCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.category:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=FormCategoryService(db).create(ctx, **body.model_dump(exclude_none=True)),
    )


@categories_router.patch("/{row_id}", response_model=APIResponse[FormCategoryResponse])
def update_category(
    row_id: UUID,
    body: FormCategoryUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.category:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=FormCategoryService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@categories_router.post("/{row_id}/archive", response_model=APIResponse[FormCategoryResponse])
def archive_category(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.category:archive"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Archived", data=FormCategoryService(db).archive(ctx, row_id))


@categories_router.post("/{row_id}/restore", response_model=APIResponse[FormCategoryResponse])
def restore_category(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.category:restore"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Restored", data=FormCategoryService(db).restore(ctx, row_id))


@categories_router.delete("/{row_id}", response_model=APIResponse[FormCategoryResponse])
def delete_category(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.category:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Archived", data=FormCategoryService(db).archive(ctx, row_id)
    )


# --- Definitions ---

definitions_router = APIRouter(prefix="/definitions", tags=["Low-Code — Definition"])


@definitions_router.get("", response_model=APIResponse[dict[str, Any]])
def list_definitions(
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.definition:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    sort: Annotated[SortParams, Depends(get_sort)],
    company_id: UUID | None = None,
    status: str | None = None,
    category_id: UUID | None = None,
    module_affinity: str | None = None,
    entity_type: str | None = None,
    search: str | None = None,
):
    page = FormDefinitionService(db).list(
        ctx,
        company_id=company_id,
        status=status,
        category_id=category_id,
        module_affinity=module_affinity,
        entity_type=entity_type,
        search=search,
        page=pagination.page,
        page_size=pagination.page_size,
        sort_by=sort.sort_by or "form_name",
        sort_dir=sort.sort_dir,
    )
    return APIResponse(message="OK", data=page_payload(page))


@definitions_router.get("/{row_id}", response_model=APIResponse[FormDefinitionResponse])
def get_definition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.definition:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=FormDefinitionService(db).get(ctx, row_id))


@definitions_router.post("", response_model=APIResponse[FormDefinitionResponse])
def create_definition(
    body: FormDefinitionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.definition:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=FormDefinitionService(db).create(ctx, **body.model_dump(exclude_none=True)),
    )


@definitions_router.patch("/{row_id}", response_model=APIResponse[FormDefinitionResponse])
def update_definition(
    row_id: UUID,
    body: FormDefinitionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.definition:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=FormDefinitionService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@definitions_router.post(
    "/{row_id}/archive", response_model=APIResponse[FormDefinitionResponse]
)
def archive_definition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.definition:archive"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Archived", data=FormDefinitionService(db).archive(ctx, row_id)
    )


@definitions_router.post(
    "/{row_id}/restore", response_model=APIResponse[FormDefinitionResponse]
)
def restore_definition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.definition:restore"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Restored", data=FormDefinitionService(db).restore(ctx, row_id)
    )


@definitions_router.get(
    "/{row_id}/versions",
    response_model=APIResponse[list[FormVersionResponse]],
)
def list_definition_versions(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.version:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
):
    items = FormVersionService(db).list_by_definition(ctx, row_id)
    start = pagination.offset
    end = start + pagination.page_size
    return APIResponse(message="OK", data=items[start:end])


# --- Versions ---

versions_router = APIRouter(prefix="/versions", tags=["Low-Code — Version"])


@versions_router.get("/{row_id}", response_model=APIResponse[FormVersionResponse])
def get_version(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.version:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=FormVersionService(db).get(ctx, row_id))


@versions_router.post("", response_model=APIResponse[FormVersionResponse])
def create_version_draft(
    body: FormVersionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.version:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    definition_id = data.pop("definition_id")
    return APIResponse(
        message="Created",
        data=FormVersionService(db).create_draft(ctx, definition_id, **data),
    )


@versions_router.patch("/{row_id}", response_model=APIResponse[FormVersionResponse])
def update_version(
    row_id: UUID,
    body: FormVersionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.version:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=FormVersionService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@versions_router.post("/{row_id}/validate-publish", response_model=APIResponse[dict[str, Any]])
def validate_publish(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.version:validate"))],
    db: Annotated[Session, Depends(get_db)],
):
    result = PublishValidationService(db).validate(ctx, row_id)
    return APIResponse(message="OK", data=result.to_dict())


@versions_router.post("/{row_id}/publish", response_model=APIResponse[FormVersionResponse])
def publish_version(
    row_id: UUID,
    body: FormVersionPublish,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.version:publish"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Published",
        data=FormVersionService(db).publish(
            ctx, row_id, publish_reason=body.publish_reason
        ),
    )


@versions_router.post("/{row_id}/retire", response_model=APIResponse[FormVersionResponse])
def retire_version(
    row_id: UUID,
    body: FormVersionRetire,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.version:retire"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Retired",
        data=FormVersionService(db).retire(ctx, row_id, retire_reason=body.retire_reason),
    )


@versions_router.post("/{row_id}/clone", response_model=APIResponse[FormVersionResponse])
def clone_version(
    row_id: UUID,
    body: FormVersionClone,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.version:clone"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Cloned",
        data=FormVersionService(db).clone_version(
            ctx,
            row_id,
            version_label=body.version_label,
            change_notes=body.change_notes,
            clone_reason=body.clone_reason,
        ),
    )


# --- Sections (Phase 2A) ---

sections_router = APIRouter(prefix="/sections", tags=["Low-Code — Section"])


@sections_router.get("", response_model=APIResponse[list[FormSectionResponse]])
def list_sections(
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.section:read"))],
    db: Annotated[Session, Depends(get_db)],
    form_version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=FormSectionService(db).list_by_version(ctx, form_version_id),
    )


@sections_router.get("/{row_id}", response_model=APIResponse[FormSectionResponse])
def get_section(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.section:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=FormSectionService(db).get(ctx, row_id))


@sections_router.post("", response_model=APIResponse[FormSectionResponse])
def create_section(
    body: FormSectionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.section:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    form_version_id = data.pop("form_version_id")
    return APIResponse(
        message="Created",
        data=FormSectionService(db).create(ctx, form_version_id, **data),
    )


@sections_router.patch("/{row_id}", response_model=APIResponse[FormSectionResponse])
def update_section(
    row_id: UUID,
    body: FormSectionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.section:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=FormSectionService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@sections_router.delete("/{row_id}", response_model=APIResponse[FormSectionResponse])
def delete_section(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.section:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=FormSectionService(db).soft_delete(ctx, row_id)
    )


# --- Fields (Phase 2A) ---

fields_router = APIRouter(prefix="/fields", tags=["Low-Code — Field"])


@fields_router.get("", response_model=APIResponse[list[FormFieldResponse]])
def list_fields(
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.field:read"))],
    db: Annotated[Session, Depends(get_db)],
    form_version_id: UUID | None = None,
    section_id: UUID | None = None,
):
    svc = FormFieldService(db)
    if section_id is not None:
        return APIResponse(message="OK", data=svc.list_by_section(ctx, section_id))
    if form_version_id is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=422, detail="form_version_id or section_id required")
    return APIResponse(message="OK", data=svc.list_by_version(ctx, form_version_id))


@fields_router.get("/{row_id}", response_model=APIResponse[FormFieldResponse])
def get_field(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.field:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=FormFieldService(db).get(ctx, row_id))


@fields_router.post("", response_model=APIResponse[FormFieldResponse])
def create_field(
    body: FormFieldCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.field:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    form_version_id = data.pop("form_version_id")
    return APIResponse(
        message="Created",
        data=FormFieldService(db).create(ctx, form_version_id, **data),
    )


@fields_router.patch("/{row_id}", response_model=APIResponse[FormFieldResponse])
def update_field(
    row_id: UUID,
    body: FormFieldUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.field:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=FormFieldService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@fields_router.delete("/{row_id}", response_model=APIResponse[FormFieldResponse])
def delete_field(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.field:delete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted", data=FormFieldService(db).soft_delete(ctx, row_id)
    )


# --- Structure validation (Phase 2A) ---

structure_router = APIRouter(prefix="/structure", tags=["Low-Code — Structure"])


@structure_router.post("/validate", response_model=APIResponse[dict[str, Any]])
def validate_structure(
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.structure:validate"))],
    db: Annotated[Session, Depends(get_db)],
    form_version_id: UUID,
):
    result = FormStructureValidationService(db).validate(ctx, form_version_id)
    return APIResponse(message="OK", data=result.to_dict())


# --- Components (Phase 2B) ---

components_router = APIRouter(prefix="/components", tags=["Low-Code — Component"])


@components_router.get("", response_model=APIResponse[dict[str, Any]])
def list_components(
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.component:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    sort: Annotated[SortParams, Depends(get_sort)],
    company_id: UUID | None = None,
    status: str | None = None,
    component_kind: str | None = None,
    search: str | None = None,
):
    page = ComponentService(db).list(
        ctx,
        company_id=company_id,
        status=status,
        component_kind=component_kind,
        search=search,
        page=pagination.page,
        page_size=pagination.page_size,
        sort_by=sort.sort_by or "component_name",
        sort_dir=sort.sort_dir,
    )
    return APIResponse(message="OK", data=page_payload(page))


@components_router.get("/{row_id}", response_model=APIResponse[ComponentResponse])
def get_component(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.component:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=ComponentService(db).get(ctx, row_id))


@components_router.post("", response_model=APIResponse[ComponentResponse])
def create_component(
    body: ComponentCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.component:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=ComponentService(db).create(ctx, **body.model_dump(exclude_none=True)),
    )


@components_router.patch("/{row_id}", response_model=APIResponse[ComponentResponse])
def update_component(
    row_id: UUID,
    body: ComponentUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.component:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=ComponentService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@components_router.post("/{row_id}/archive", response_model=APIResponse[ComponentResponse])
def archive_component(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.component:archive"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Archived", data=ComponentService(db).archive(ctx, row_id))


@components_router.post("/{row_id}/restore", response_model=APIResponse[ComponentResponse])
def restore_component(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.component:restore"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="Restored", data=ComponentService(db).restore(ctx, row_id))


@components_router.get(
    "/{row_id}/versions",
    response_model=APIResponse[list[ComponentVersionResponse]],
)
def list_component_versions(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.component_version:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
):
    items = ComponentVersionService(db).list_by_component(ctx, row_id)
    start = pagination.offset
    end = start + pagination.page_size
    return APIResponse(message="OK", data=items[start:end])


# --- Component Versions (Phase 2B) ---

component_versions_router = APIRouter(
    prefix="/component-versions", tags=["Low-Code — Component Version"]
)


@component_versions_router.get(
    "/{row_id}", response_model=APIResponse[ComponentVersionResponse]
)
def get_component_version(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.component_version:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=ComponentVersionService(db).get(ctx, row_id))


@component_versions_router.post("", response_model=APIResponse[ComponentVersionResponse])
def create_component_version_draft(
    body: ComponentVersionCreate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.component_version:create"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    component_id = data.pop("component_id")
    return APIResponse(
        message="Created",
        data=ComponentVersionService(db).create_draft(ctx, component_id, **data),
    )


@component_versions_router.patch(
    "/{row_id}", response_model=APIResponse[ComponentVersionResponse]
)
def update_component_version(
    row_id: UUID,
    body: ComponentVersionUpdate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.component_version:update"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=ComponentVersionService(db).update(
            ctx, row_id, **extract_update_fields(body)
        ),
    )


@component_versions_router.post(
    "/{row_id}/publish", response_model=APIResponse[ComponentVersionResponse]
)
def publish_component_version(
    row_id: UUID,
    body: ComponentVersionPublish,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.component_version:publish"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Published",
        data=ComponentVersionService(db).publish(
            ctx, row_id, publish_reason=body.publish_reason
        ),
    )


@component_versions_router.post(
    "/{row_id}/retire", response_model=APIResponse[ComponentVersionResponse]
)
def retire_component_version(
    row_id: UUID,
    body: ComponentVersionRetire,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.component_version:retire"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Retired",
        data=ComponentVersionService(db).retire(
            ctx, row_id, retire_reason=body.retire_reason
        ),
    )


@component_versions_router.post(
    "/{row_id}/clone", response_model=APIResponse[ComponentVersionResponse]
)
def clone_component_version(
    row_id: UUID,
    body: ComponentVersionClone,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.component_version:clone"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Cloned",
        data=ComponentVersionService(db).clone_version(
            ctx,
            row_id,
            version_label=body.version_label,
            change_notes=body.change_notes,
            clone_reason=body.clone_reason,
        ),
    )


# --- Data Sources (Phase 2C) ---

data_sources_router = APIRouter(prefix="/data-sources", tags=["Low-Code — Data Source"])


@data_sources_router.get("", response_model=APIResponse[dict[str, Any]])
def list_data_sources(
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.data_source:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    sort: Annotated[SortParams, Depends(get_sort)],
    company_id: UUID | None = None,
    status: str | None = None,
    module_code: str | None = None,
    entity_type: str | None = None,
    search: str | None = None,
):
    page = DataSourceService(db).list(
        ctx,
        company_id=company_id,
        status=status,
        module_code=module_code,
        entity_type=entity_type,
        search=search,
        page=pagination.page,
        page_size=pagination.page_size,
        sort_by=sort.sort_by or "data_source_name",
        sort_dir=sort.sort_dir,
    )
    return APIResponse(message="OK", data=page_payload(page))


@data_sources_router.get("/{row_id}", response_model=APIResponse[DataSourceResponse])
def get_data_source(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.data_source:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=DataSourceService(db).get(ctx, row_id))


@data_sources_router.post("", response_model=APIResponse[DataSourceResponse])
def create_data_source(
    body: DataSourceCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.data_source:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=DataSourceService(db).create(ctx, **body.model_dump(exclude_none=True)),
    )


@data_sources_router.patch("/{row_id}", response_model=APIResponse[DataSourceResponse])
def update_data_source(
    row_id: UUID,
    body: DataSourceUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.data_source:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=DataSourceService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@data_sources_router.post(
    "/{row_id}/archive", response_model=APIResponse[DataSourceResponse]
)
def archive_data_source(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.data_source:archive"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Archived", data=DataSourceService(db).archive(ctx, row_id)
    )


@data_sources_router.post(
    "/{row_id}/restore", response_model=APIResponse[DataSourceResponse]
)
def restore_data_source(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.data_source:restore"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Restored", data=DataSourceService(db).restore(ctx, row_id)
    )


@data_sources_router.post(
    "/{row_id}/activate", response_model=APIResponse[DataSourceResponse]
)
def activate_data_source(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.data_source:activate"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Activated", data=DataSourceService(db).activate(ctx, row_id)
    )


@data_sources_router.post(
    "/{row_id}/retire", response_model=APIResponse[DataSourceResponse]
)
def retire_data_source(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.data_source:retire"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Retired", data=DataSourceService(db).retire(ctx, row_id)
    )


# --- Expressions (Phase 2C) ---

expressions_router = APIRouter(prefix="/expressions", tags=["Low-Code — Expression"])


@expressions_router.get("", response_model=APIResponse[dict[str, Any]])
def list_expressions(
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.expression:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    sort: Annotated[SortParams, Depends(get_sort)],
    company_id: UUID | None = None,
    status: str | None = None,
    expression_kind: str | None = None,
    search: str | None = None,
):
    page = ExpressionService(db).list(
        ctx,
        company_id=company_id,
        status=status,
        expression_kind=expression_kind,
        search=search,
        page=pagination.page,
        page_size=pagination.page_size,
        sort_by=sort.sort_by or "expression_name",
        sort_dir=sort.sort_dir,
    )
    return APIResponse(message="OK", data=page_payload(page))


@expressions_router.get("/{row_id}", response_model=APIResponse[ExpressionResponse])
def get_expression(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.expression:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=ExpressionService(db).get(ctx, row_id))


@expressions_router.post("", response_model=APIResponse[ExpressionResponse])
def create_expression(
    body: ExpressionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.expression:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=ExpressionService(db).create(ctx, **body.model_dump(exclude_none=True)),
    )


@expressions_router.patch("/{row_id}", response_model=APIResponse[ExpressionResponse])
def update_expression(
    row_id: UUID,
    body: ExpressionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.expression:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=ExpressionService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@expressions_router.post("/{row_id}/archive", response_model=APIResponse[ExpressionResponse])
def archive_expression(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.expression:archive"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Archived", data=ExpressionService(db).archive(ctx, row_id)
    )


@expressions_router.post("/{row_id}/restore", response_model=APIResponse[ExpressionResponse])
def restore_expression(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.expression:restore"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Restored", data=ExpressionService(db).restore(ctx, row_id)
    )


@expressions_router.post("/{row_id}/publish", response_model=APIResponse[ExpressionResponse])
def publish_expression(
    row_id: UUID,
    body: ExpressionPublish,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.expression:publish"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Published",
        data=ExpressionService(db).publish(
            ctx, row_id, publish_reason=body.publish_reason
        ),
    )


@expressions_router.post("/{row_id}/retire", response_model=APIResponse[ExpressionResponse])
def retire_expression(
    row_id: UUID,
    body: ExpressionRetire,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.expression:retire"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Retired",
        data=ExpressionService(db).retire(ctx, row_id, retire_reason=body.retire_reason),
    )


@expressions_router.get(
    "/{row_id}/bindings",
    response_model=APIResponse[list[ExpressionBindingResponse]],
)
def list_expression_bindings(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.expression_binding:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK",
        data=ExpressionBindingService(db).list_by_expression(ctx, row_id),
    )


# --- Expression Bindings (Phase 2C) ---

expression_bindings_router = APIRouter(
    prefix="/expression-bindings", tags=["Low-Code — Expression Binding"]
)


@expression_bindings_router.get(
    "", response_model=APIResponse[list[ExpressionBindingResponse]]
)
def list_bindings_by_form_version(
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.expression_binding:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
    form_version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=ExpressionBindingService(db).list_by_form_version(ctx, form_version_id),
    )


@expression_bindings_router.get(
    "/{row_id}", response_model=APIResponse[ExpressionBindingResponse]
)
def get_expression_binding(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.expression_binding:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK", data=ExpressionBindingService(db).get(ctx, row_id)
    )


@expression_bindings_router.post(
    "", response_model=APIResponse[ExpressionBindingResponse]
)
def create_expression_binding(
    body: ExpressionBindingCreate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.expression_binding:create"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=ExpressionBindingService(db).create(
            ctx, **body.model_dump(exclude_none=True)
        ),
    )


@expression_bindings_router.patch(
    "/{row_id}", response_model=APIResponse[ExpressionBindingResponse]
)
def update_expression_binding(
    row_id: UUID,
    body: ExpressionBindingUpdate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.expression_binding:update"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=ExpressionBindingService(db).update(
            ctx, row_id, **extract_update_fields(body)
        ),
    )


@expression_bindings_router.delete(
    "/{row_id}", response_model=APIResponse[ExpressionBindingResponse]
)
def delete_expression_binding(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.expression_binding:delete"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted",
        data=ExpressionBindingService(db).soft_delete(ctx, row_id),
    )


# --- Event Handlers (Phase 3A) ---

event_handlers_router = APIRouter(
    prefix="/event-handlers", tags=["Low-Code — Event Handler"]
)


@event_handlers_router.get("", response_model=APIResponse[list[EventHandlerResponse]])
def list_event_handlers(
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.event_handler:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
    form_version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=EventHandlerService(db).list_by_form_version(ctx, form_version_id),
    )


@event_handlers_router.get(
    "/{row_id}", response_model=APIResponse[EventHandlerResponse]
)
def get_event_handler(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.event_handler:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=EventHandlerService(db).get(ctx, row_id))


@event_handlers_router.post("", response_model=APIResponse[EventHandlerResponse])
def create_event_handler(
    body: EventHandlerCreate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.event_handler:create"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=EventHandlerService(db).create(ctx, **body.model_dump(exclude_none=True)),
    )


@event_handlers_router.patch(
    "/{row_id}", response_model=APIResponse[EventHandlerResponse]
)
def update_event_handler(
    row_id: UUID,
    body: EventHandlerUpdate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.event_handler:update"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=EventHandlerService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@event_handlers_router.delete(
    "/{row_id}", response_model=APIResponse[EventHandlerResponse]
)
def delete_event_handler(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.event_handler:delete"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted",
        data=EventHandlerService(db).soft_delete(ctx, row_id),
    )


# --- Localization Entries (Phase 3A) ---

localization_entries_router = APIRouter(
    prefix="/localization-entries", tags=["Low-Code — Localization"]
)


@localization_entries_router.get(
    "", response_model=APIResponse[list[LocalizationEntryResponse]]
)
def list_localization_entries(
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.localization:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
    form_version_id: UUID | None = None,
    owner_type: str | None = None,
    owner_ref_id: UUID | None = None,
):
    svc = LocalizationEntryService(db)
    if owner_type is not None and owner_ref_id is not None:
        return APIResponse(
            message="OK",
            data=svc.list_by_owner(ctx, owner_type, owner_ref_id),
        )
    if form_version_id is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=422,
            detail="form_version_id or (owner_type + owner_ref_id) required",
        )
    return APIResponse(
        message="OK",
        data=svc.list_by_form_version(ctx, form_version_id),
    )


@localization_entries_router.get(
    "/{row_id}", response_model=APIResponse[LocalizationEntryResponse]
)
def get_localization_entry(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.localization:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK", data=LocalizationEntryService(db).get(ctx, row_id)
    )


@localization_entries_router.post(
    "", response_model=APIResponse[LocalizationEntryResponse]
)
def create_localization_entry(
    body: LocalizationEntryCreate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.localization:create"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=LocalizationEntryService(db).create(
            ctx, **body.model_dump(exclude_none=True)
        ),
    )


@localization_entries_router.patch(
    "/{row_id}", response_model=APIResponse[LocalizationEntryResponse]
)
def update_localization_entry(
    row_id: UUID,
    body: LocalizationEntryUpdate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.localization:update"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=LocalizationEntryService(db).update(
            ctx, row_id, **extract_update_fields(body)
        ),
    )


@localization_entries_router.delete(
    "/{row_id}", response_model=APIResponse[LocalizationEntryResponse]
)
def delete_localization_entry(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.localization:delete"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted",
        data=LocalizationEntryService(db).soft_delete(ctx, row_id),
    )


@localization_entries_router.post(
    "/{row_id}/publish", response_model=APIResponse[LocalizationEntryResponse]
)
def publish_localization_entry(
    row_id: UUID,
    body: LocalizationEntryPublish,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.localization:publish"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Published",
        data=LocalizationEntryService(db).publish(
            ctx, row_id, publish_reason=body.publish_reason
        ),
    )


@localization_entries_router.post(
    "/{row_id}/retire", response_model=APIResponse[LocalizationEntryResponse]
)
def retire_localization_entry(
    row_id: UUID,
    body: LocalizationEntryRetire,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.localization:retire"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Retired",
        data=LocalizationEntryService(db).retire(
            ctx, row_id, retire_reason=body.retire_reason
        ),
    )


# --- Page Definitions (Phase 3B) ---

page_definitions_router = APIRouter(
    prefix="/pages", tags=["Low-Code — Page Definition"]
)


@page_definitions_router.get("", response_model=APIResponse[dict[str, Any]])
def list_page_definitions(
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.page:read"))],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
    sort: Annotated[SortParams, Depends(get_sort)],
    company_id: UUID | None = None,
    status: str | None = None,
    category_id: UUID | None = None,
    search: str | None = None,
):
    page = PageDefinitionService(db).list(
        ctx,
        company_id=company_id,
        status=status,
        category_id=category_id,
        search=search,
        page=pagination.page,
        page_size=pagination.page_size,
        sort_by=sort.sort_by or "page_name",
        sort_dir=sort.sort_dir,
    )
    return APIResponse(message="OK", data=page_payload(page))


@page_definitions_router.get("/{row_id}", response_model=APIResponse[PageDefinitionResponse])
def get_page_definition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.page:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=PageDefinitionService(db).get(ctx, row_id))


@page_definitions_router.post("", response_model=APIResponse[PageDefinitionResponse])
def create_page_definition(
    body: PageDefinitionCreate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.page:create"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=PageDefinitionService(db).create(ctx, **body.model_dump(exclude_none=True)),
    )


@page_definitions_router.patch(
    "/{row_id}", response_model=APIResponse[PageDefinitionResponse]
)
def update_page_definition(
    row_id: UUID,
    body: PageDefinitionUpdate,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.page:update"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=PageDefinitionService(db).update(
            ctx, row_id, **extract_update_fields(body)
        ),
    )


@page_definitions_router.post(
    "/{row_id}/archive", response_model=APIResponse[PageDefinitionResponse]
)
def archive_page_definition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.page:archive"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Archived", data=PageDefinitionService(db).archive(ctx, row_id)
    )


@page_definitions_router.post(
    "/{row_id}/restore", response_model=APIResponse[PageDefinitionResponse]
)
def restore_page_definition(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("lowcode.page:restore"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Restored", data=PageDefinitionService(db).restore(ctx, row_id)
    )


@page_definitions_router.get(
    "/{row_id}/versions",
    response_model=APIResponse[list[PageVersionResponse]],
)
def list_page_definition_versions(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_version:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
    pagination: Annotated[PaginationParams, Depends(get_pagination)],
):
    items = PageVersionService(db).list_by_definition(ctx, row_id)
    start = pagination.offset
    end = start + pagination.page_size
    return APIResponse(message="OK", data=items[start:end])


# --- Page Versions (Phase 3B) ---

page_versions_router = APIRouter(
    prefix="/page-versions", tags=["Low-Code — Page Version"]
)


@page_versions_router.get("/{row_id}", response_model=APIResponse[PageVersionResponse])
def get_page_version(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_version:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=PageVersionService(db).get(ctx, row_id))


@page_versions_router.post("", response_model=APIResponse[PageVersionResponse])
def create_page_version_draft(
    body: PageVersionCreate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_version:create"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    definition_id = data.pop("definition_id")
    return APIResponse(
        message="Created",
        data=PageVersionService(db).create_draft(ctx, definition_id, **data),
    )


@page_versions_router.patch("/{row_id}", response_model=APIResponse[PageVersionResponse])
def update_page_version(
    row_id: UUID,
    body: PageVersionUpdate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_version:update"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=PageVersionService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@page_versions_router.post(
    "/{row_id}/publish", response_model=APIResponse[PageVersionResponse]
)
def publish_page_version(
    row_id: UUID,
    body: PageVersionPublish,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_version:publish"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Published",
        data=PageVersionService(db).publish(
            ctx, row_id, publish_reason=body.publish_reason
        ),
    )


@page_versions_router.post(
    "/{row_id}/retire", response_model=APIResponse[PageVersionResponse]
)
def retire_page_version(
    row_id: UUID,
    body: PageVersionRetire,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_version:retire"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Retired",
        data=PageVersionService(db).retire(
            ctx, row_id, retire_reason=body.retire_reason
        ),
    )


@page_versions_router.post(
    "/{row_id}/clone", response_model=APIResponse[PageVersionResponse]
)
def clone_page_version(
    row_id: UUID,
    body: PageVersionClone,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_version:clone"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Cloned",
        data=PageVersionService(db).clone_version(
            ctx,
            row_id,
            version_label=body.version_label,
            change_notes=body.change_notes,
            clone_reason=body.clone_reason,
        ),
    )


# --- Page Regions (Phase 3B) ---

page_regions_router = APIRouter(
    prefix="/page-regions", tags=["Low-Code — Page Region"]
)


@page_regions_router.get("", response_model=APIResponse[list[PageRegionResponse]])
def list_page_regions(
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_region:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
    page_version_id: UUID,
):
    return APIResponse(
        message="OK",
        data=PageRegionService(db).list_by_version(ctx, page_version_id),
    )


@page_regions_router.get("/{row_id}", response_model=APIResponse[PageRegionResponse])
def get_page_region(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_region:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=PageRegionService(db).get(ctx, row_id))


@page_regions_router.post("", response_model=APIResponse[PageRegionResponse])
def create_page_region(
    body: PageRegionCreate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_region:create"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    data = body.model_dump(exclude_none=True)
    page_version_id = data.pop("page_version_id")
    return APIResponse(
        message="Created",
        data=PageRegionService(db).create(ctx, page_version_id, **data),
    )


@page_regions_router.patch("/{row_id}", response_model=APIResponse[PageRegionResponse])
def update_page_region(
    row_id: UUID,
    body: PageRegionUpdate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_region:update"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=PageRegionService(db).update(ctx, row_id, **extract_update_fields(body)),
    )


@page_regions_router.delete("/{row_id}", response_model=APIResponse[PageRegionResponse])
def delete_page_region(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.page_region:delete"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Deleted",
        data=PageRegionService(db).soft_delete(ctx, row_id),
    )


# --- Publish History (Phase 4) ---

publish_history_router = APIRouter(
    prefix="/publish-history", tags=["Low-Code — Publish History"]
)


@publish_history_router.get(
    "/by-form/{form_definition_id}",
    response_model=APIResponse[list[PublishHistoryResponse]],
)
def list_publish_history_by_form(
    form_definition_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.publish_history:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK",
        data=PublishHistoryService(db).list_by_form_definition(
            ctx, form_definition_id
        ),
    )


@publish_history_router.get(
    "/by-page/{page_definition_id}",
    response_model=APIResponse[list[PublishHistoryResponse]],
)
def list_publish_history_by_page(
    page_definition_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.publish_history:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK",
        data=PublishHistoryService(db).list_by_page_definition(
            ctx, page_definition_id
        ),
    )


@publish_history_router.get(
    "/{row_id}", response_model=APIResponse[PublishHistoryResponse]
)
def get_publish_history(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.publish_history:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK", data=PublishHistoryService(db).get(ctx, row_id)
    )


# --- Runtime Submissions (Phase 4) ---

runtime_submissions_router = APIRouter(
    prefix="/runtime-submissions", tags=["Low-Code — Runtime Submission"]
)


@runtime_submissions_router.get(
    "", response_model=APIResponse[list[RuntimeSubmissionResponse]]
)
def list_runtime_submissions(
    module_code: str,
    entity_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.runtime_submission:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK",
        data=RuntimeSubmissionService(db).list_by_module_entity(
            ctx, module_code, entity_id
        ),
    )


@runtime_submissions_router.get(
    "/by-correlation/{correlation_id}",
    response_model=APIResponse[RuntimeSubmissionResponse],
)
def get_runtime_submission_by_correlation(
    correlation_id: str,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.runtime_submission:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
    company_id: UUID | None = None,
):
    return APIResponse(
        message="OK",
        data=RuntimeSubmissionService(db).get_by_correlation(
            ctx, correlation_id, company_id=company_id
        ),
    )


@runtime_submissions_router.get(
    "/{row_id}", response_model=APIResponse[RuntimeSubmissionResponse]
)
def get_runtime_submission(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.runtime_submission:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK", data=RuntimeSubmissionService(db).get(ctx, row_id)
    )


@runtime_submissions_router.post(
    "", response_model=APIResponse[RuntimeSubmissionResponse]
)
def create_runtime_submission(
    body: RuntimeSubmissionCreate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.runtime_submission:create"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=RuntimeSubmissionService(db).create(
            ctx, **extract_update_fields(body)
        ),
    )


@runtime_submissions_router.patch(
    "/{row_id}/status", response_model=APIResponse[RuntimeSubmissionResponse]
)
def update_runtime_submission_status(
    row_id: UUID,
    body: RuntimeSubmissionStatusUpdate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.runtime_submission:update"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Updated",
        data=RuntimeSubmissionService(db).update_status(
            ctx,
            row_id,
            submission_status=body.submission_status,
            validation_result_json=body.validation_result_json,
            metadata_json=body.metadata_json,
        ),
    )


# --- Preview Sessions (Phase 4) ---

preview_sessions_router = APIRouter(
    prefix="/preview-sessions", tags=["Low-Code — Preview Session"]
)


@preview_sessions_router.get(
    "", response_model=APIResponse[list[PreviewSessionResponse]]
)
def list_preview_sessions(
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.preview_session:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
    designer_user_id: UUID | None = None,
):
    return APIResponse(
        message="OK",
        data=PreviewSessionService(db).list_by_designer(ctx, designer_user_id),
    )


@preview_sessions_router.get(
    "/{row_id}", response_model=APIResponse[PreviewSessionResponse]
)
def get_preview_session(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.preview_session:read"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK", data=PreviewSessionService(db).get(ctx, row_id)
    )


@preview_sessions_router.post(
    "", response_model=APIResponse[PreviewSessionResponse]
)
def create_preview_session(
    body: PreviewSessionCreate,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.preview_session:create"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Created",
        data=PreviewSessionService(db).create(ctx, **extract_update_fields(body)),
    )


@preview_sessions_router.post(
    "/{row_id}/close", response_model=APIResponse[PreviewSessionResponse]
)
def close_preview_session(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.preview_session:close"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Closed", data=PreviewSessionService(db).close(ctx, row_id)
    )


@preview_sessions_router.post(
    "/{row_id}/expire", response_model=APIResponse[PreviewSessionResponse]
)
def expire_preview_session(
    row_id: UUID,
    ctx: Annotated[
        TenantContext, Depends(require_permission("lowcode.preview_session:expire"))
    ],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Expired", data=PreviewSessionService(db).expire(ctx, row_id)
    )
