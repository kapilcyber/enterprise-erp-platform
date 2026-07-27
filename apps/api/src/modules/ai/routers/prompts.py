"""AI prompt routers — template, version, variable."""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.ai.dependencies import get_db, require_permission
from modules.ai.routers._common import (
    _app,
    register_lifecycle_route,
    register_standard_crud,
)
from modules.ai.schemas import (
    CloneBody,
    PromptTemplateCreate,
    PromptTemplateResponse,
    PromptTemplateUpdate,
    PromptVariableCreate,
    PromptVariableResponse,
    PromptVariableUpdate,
    PromptVersionCreate,
    PromptVersionResponse,
    PromptVersionUpdate,
    PublishBody,
    RetireBody,
)
from modules.foundation.domain.value_objects import TenantContext
from shared.schemas import APIResponse

prompt_templates_router = APIRouter(prefix="/prompt-templates", tags=["AI — Prompt Template"])
prompt_versions_router = APIRouter(prefix="/prompt-versions", tags=["AI — Prompt Version"])
prompt_variables_router = APIRouter(prefix="/prompt-variables", tags=["AI — Prompt Variable"])

register_standard_crud(
    prompt_templates_router,
    resource="prompt_template",
    service_attr="prompt_templates",
    create_schema=PromptTemplateCreate,
    update_schema=PromptTemplateUpdate,
    response_schema=PromptTemplateResponse,
    default_sort="template_name",
    tag="AI — Prompt Template",
)


def _create_prompt_version_draft(ctx, db, body: PromptVersionCreate):
    data = body.model_dump(exclude_none=True)
    template_id = data.pop("template_id")
    return APIResponse(
        message="Created",
        data=_app(db).prompt_versions.create_draft(ctx, template_id, **data),
    )


register_standard_crud(
    prompt_versions_router,
    resource="prompt_version",
    service_attr="prompt_versions",
    create_schema=PromptVersionCreate,
    update_schema=PromptVersionUpdate,
    response_schema=PromptVersionResponse,
    default_sort="version_number",
    tag="AI — Prompt Version",
    create_handler=_create_prompt_version_draft,
)
register_lifecycle_route(
    prompt_versions_router,
    path="/{row_id}/publish",
    resource="prompt_version",
    action="publish",
    service_attr="prompt_versions",
    method_name="publish",
    response_schema=PromptVersionResponse,
    tag="AI — Prompt Version",
    body_schema=PublishBody,
    message="Published",
)
register_lifecycle_route(
    prompt_versions_router,
    path="/{row_id}/retire",
    resource="prompt_version",
    action="retire",
    service_attr="prompt_versions",
    method_name="retire",
    response_schema=PromptVersionResponse,
    tag="AI — Prompt Version",
    body_schema=RetireBody,
    message="Retired",
)
register_lifecycle_route(
    prompt_versions_router,
    path="/{row_id}/clone",
    resource="prompt_version",
    action="create",
    service_attr="prompt_versions",
    method_name="clone_version",
    response_schema=PromptVersionResponse,
    tag="AI — Prompt Version",
    body_schema=CloneBody,
    message="Cloned",
)


@prompt_versions_router.post(
    "/{row_id}/validate-publish",
    response_model=APIResponse[dict[str, Any]],
    tags=["AI — Prompt Version"],
)
def validate_publish_prompt_version(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.prompt_version:validate"))],
    db: Annotated[Session, Depends(get_db)],
):
    result = _app(db).publish_validation.validate(ctx, row_id)
    payload = result.to_dict() if hasattr(result, "to_dict") else result
    return APIResponse(message="OK", data=payload)


register_standard_crud(
    prompt_variables_router,
    resource="prompt_variable",
    service_attr="prompt_variables",
    create_schema=PromptVariableCreate,
    update_schema=PromptVariableUpdate,
    response_schema=PromptVariableResponse,
    default_sort="variable_code",
    tag="AI — Prompt Variable",
)
