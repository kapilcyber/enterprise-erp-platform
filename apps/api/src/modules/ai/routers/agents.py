"""AI agents & tools metadata routers — Phase 3 (NO invoke/execute)."""

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
    AgentCreate,
    AgentResponse,
    AgentUpdate,
    AgentVersionCreate,
    AgentVersionResponse,
    AgentVersionUpdate,
    CloneBody,
    PublishBody,
    RetireBody,
    SkillCreate,
    SkillResponse,
    SkillUpdate,
    ToolCreate,
    ToolResponse,
    ToolUpdate,
    ToolVersionCreate,
    ToolVersionResponse,
    ToolVersionUpdate,
)
from modules.foundation.domain.value_objects import TenantContext
from shared.schemas import APIResponse

tools_router = APIRouter(prefix="/tools", tags=["AI — Tool"])
tool_versions_router = APIRouter(prefix="/tool-versions", tags=["AI — Tool Version"])
skills_router = APIRouter(prefix="/skills", tags=["AI — Skill"])
agents_router = APIRouter(prefix="/agents", tags=["AI — Agent"])
agent_versions_router = APIRouter(prefix="/agent-versions", tags=["AI — Agent Version"])

register_standard_crud(
    tools_router,
    resource="tool",
    service_attr="tools",
    create_schema=ToolCreate,
    update_schema=ToolUpdate,
    response_schema=ToolResponse,
    default_sort="tool_name",
    tag="AI — Tool",
)
register_lifecycle_route(
    tools_router,
    path="/{row_id}/publish",
    resource="tool",
    action="publish",
    service_attr="tools",
    method_name="publish",
    response_schema=ToolResponse,
    tag="AI — Tool",
    body_schema=PublishBody,
    message="Published",
)
register_lifecycle_route(
    tools_router,
    path="/{row_id}/retire",
    resource="tool",
    action="retire",
    service_attr="tools",
    method_name="retire",
    response_schema=ToolResponse,
    tag="AI — Tool",
    body_schema=RetireBody,
    message="Retired",
)


def _create_tool_version_draft(ctx, db, body: ToolVersionCreate):
    data = body.model_dump(exclude_none=True)
    tool_id = data.pop("tool_id")
    return APIResponse(
        message="Created",
        data=_app(db).tool_versions.create_draft(ctx, tool_id, **data),
    )


register_standard_crud(
    tool_versions_router,
    resource="tool_version",
    service_attr="tool_versions",
    create_schema=ToolVersionCreate,
    update_schema=ToolVersionUpdate,
    response_schema=ToolVersionResponse,
    default_sort="version_number",
    tag="AI — Tool Version",
    create_handler=_create_tool_version_draft,
)
register_lifecycle_route(
    tool_versions_router,
    path="/{row_id}/publish",
    resource="tool_version",
    action="publish",
    service_attr="tool_versions",
    method_name="publish",
    response_schema=ToolVersionResponse,
    tag="AI — Tool Version",
    body_schema=PublishBody,
    message="Published",
)
register_lifecycle_route(
    tool_versions_router,
    path="/{row_id}/retire",
    resource="tool_version",
    action="retire",
    service_attr="tool_versions",
    method_name="retire",
    response_schema=ToolVersionResponse,
    tag="AI — Tool Version",
    body_schema=RetireBody,
    message="Retired",
)
register_lifecycle_route(
    tool_versions_router,
    path="/{row_id}/clone",
    resource="tool_version",
    action="create",
    service_attr="tool_versions",
    method_name="clone_version",
    response_schema=ToolVersionResponse,
    tag="AI — Tool Version",
    body_schema=CloneBody,
    message="Cloned",
)


@tool_versions_router.post(
    "/{row_id}/validate-publish",
    response_model=APIResponse[dict[str, Any]],
    tags=["AI — Tool Version"],
)
def validate_publish_tool_version(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.tool_version:validate"))],
    db: Annotated[Session, Depends(get_db)],
):
    result = _app(db).publish_validation.validate_tool_version(ctx, row_id)
    return APIResponse(message="OK", data=result.to_dict())


register_standard_crud(
    skills_router,
    resource="skill",
    service_attr="skills",
    create_schema=SkillCreate,
    update_schema=SkillUpdate,
    response_schema=SkillResponse,
    default_sort="skill_name",
    tag="AI — Skill",
)
register_lifecycle_route(
    skills_router,
    path="/{row_id}/publish",
    resource="skill",
    action="publish",
    service_attr="skills",
    method_name="publish",
    response_schema=SkillResponse,
    tag="AI — Skill",
    body_schema=PublishBody,
    message="Published",
)
register_lifecycle_route(
    skills_router,
    path="/{row_id}/retire",
    resource="skill",
    action="retire",
    service_attr="skills",
    method_name="retire",
    response_schema=SkillResponse,
    tag="AI — Skill",
    body_schema=RetireBody,
    message="Retired",
)


@skills_router.post(
    "/{row_id}/validate-publish",
    response_model=APIResponse[dict[str, Any]],
    tags=["AI — Skill"],
)
def validate_publish_skill(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.skill:validate"))],
    db: Annotated[Session, Depends(get_db)],
):
    result = _app(db).publish_validation.validate_skill(ctx, row_id)
    return APIResponse(
        message="OK",
        data={
            "valid": result.valid,
            "skill_id": str(result.skill_id),
            "issues": [{"code": i.code, "message": i.message} for i in result.issues],
            "warnings": [{"code": w.code, "message": w.message} for w in result.warnings],
        },
    )


register_standard_crud(
    agents_router,
    resource="agent",
    service_attr="agents",
    create_schema=AgentCreate,
    update_schema=AgentUpdate,
    response_schema=AgentResponse,
    default_sort="agent_name",
    tag="AI — Agent",
)
register_lifecycle_route(
    agents_router,
    path="/{row_id}/activate",
    resource="agent",
    action="update",
    service_attr="agents",
    method_name="activate",
    response_schema=AgentResponse,
    tag="AI — Agent",
    message="Activated",
)
register_lifecycle_route(
    agents_router,
    path="/{row_id}/deactivate",
    resource="agent",
    action="update",
    service_attr="agents",
    method_name="deactivate",
    response_schema=AgentResponse,
    tag="AI — Agent",
    message="Deactivated",
)


def _create_agent_version_draft(ctx, db, body: AgentVersionCreate):
    data = body.model_dump(exclude_none=True)
    agent_id = data.pop("agent_id")
    return APIResponse(
        message="Created",
        data=_app(db).agent_versions.create_draft(ctx, agent_id, **data),
    )


register_standard_crud(
    agent_versions_router,
    resource="agent_version",
    service_attr="agent_versions",
    create_schema=AgentVersionCreate,
    update_schema=AgentVersionUpdate,
    response_schema=AgentVersionResponse,
    default_sort="version_number",
    tag="AI — Agent Version",
    create_handler=_create_agent_version_draft,
)
register_lifecycle_route(
    agent_versions_router,
    path="/{row_id}/publish",
    resource="agent_version",
    action="publish",
    service_attr="agent_versions",
    method_name="publish",
    response_schema=AgentVersionResponse,
    tag="AI — Agent Version",
    body_schema=PublishBody,
    message="Published",
)
register_lifecycle_route(
    agent_versions_router,
    path="/{row_id}/retire",
    resource="agent_version",
    action="retire",
    service_attr="agent_versions",
    method_name="retire",
    response_schema=AgentVersionResponse,
    tag="AI — Agent Version",
    body_schema=RetireBody,
    message="Retired",
)
register_lifecycle_route(
    agent_versions_router,
    path="/{row_id}/clone",
    resource="agent_version",
    action="create",
    service_attr="agent_versions",
    method_name="clone_version",
    response_schema=AgentVersionResponse,
    tag="AI — Agent Version",
    body_schema=CloneBody,
    message="Cloned",
)


@agent_versions_router.post(
    "/{row_id}/validate-publish",
    response_model=APIResponse[dict[str, Any]],
    tags=["AI — Agent Version"],
)
def validate_publish_agent_version(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.agent_version:validate"))],
    db: Annotated[Session, Depends(get_db)],
):
    result = _app(db).publish_validation.validate_agent_version(ctx, row_id)
    return APIResponse(
        message="OK",
        data={
            "valid": result.valid,
            "agent_version_id": str(result.agent_version_id),
            "agent_id": str(result.agent_id),
            "issues": [{"code": i.code, "message": i.message} for i in result.issues],
            "warnings": [{"code": w.code, "message": w.message} for w in result.warnings],
        },
    )


@agent_versions_router.get(
    "/{row_id}/allowed-tools",
    response_model=APIResponse[dict[str, Any]],
    tags=["AI — Agent Version"],
)
def list_allowed_tools(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.agent_version:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK",
        data=_app(db).tool_registry.list_allowed_tools_for_agent_version(ctx, row_id),
    )


@agent_versions_router.get(
    "/{row_id}/design",
    response_model=APIResponse[dict[str, Any]],
    tags=["AI — Agent Version"],
)
def get_agent_design(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.agent_version:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(message="OK", data=_app(db).agent_design.get_design_snapshot(ctx, row_id))
