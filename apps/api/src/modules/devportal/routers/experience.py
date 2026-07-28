"""Developer Portal Phase 3 documentation / sandbox / try-it routers."""

from fastapi import APIRouter

from modules.devportal.routers._common import register_lifecycle_route, register_standard_crud
from modules.devportal.schemas import (
    DocumentationEntryCreate,
    DocumentationEntryResponse,
    DocumentationEntryUpdate,
    LifecycleReason,
    OpenapiArtifactReferenceCreate,
    OpenapiArtifactReferenceResponse,
    OpenapiArtifactReferenceUpdate,
    SandboxEnvironmentCreate,
    SandboxEnvironmentResponse,
    SandboxEnvironmentUpdate,
    TryitSessionCreate,
    TryitSessionResponse,
    TryitSessionUpdate,
)

documentation_entries_router = APIRouter(
    prefix="/documentation-entries", tags=["DevPortal — Documentation"]
)
openapi_artifact_references_router = APIRouter(
    prefix="/openapi-artifact-references", tags=["DevPortal — OpenAPI Artifact"]
)
sandbox_environments_router = APIRouter(
    prefix="/sandbox-environments", tags=["DevPortal — Sandbox"]
)
tryit_sessions_router = APIRouter(prefix="/tryit-sessions", tags=["DevPortal — Try-it"])

register_standard_crud(
    documentation_entries_router,
    resource="documentation_entry",
    service_attr="documentation_entries",
    create_schema=DocumentationEntryCreate,
    update_schema=DocumentationEntryUpdate,
    response_schema=DocumentationEntryResponse,
    default_sort="title",
    tag="DevPortal — Documentation",
)
register_lifecycle_route(
    documentation_entries_router,
    path="/{row_id}/publish",
    resource="documentation_entry",
    action="publish",
    service_attr="documentation_entries",
    method_name="publish",
    response_schema=DocumentationEntryResponse,
    tag="DevPortal — Documentation",
    message="Published",
)
register_lifecycle_route(
    documentation_entries_router,
    path="/{row_id}/retire",
    resource="documentation_entry",
    action="retire",
    service_attr="documentation_entries",
    method_name="retire",
    response_schema=DocumentationEntryResponse,
    tag="DevPortal — Documentation",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    openapi_artifact_references_router,
    resource="openapi_artifact_reference",
    service_attr="openapi_artifact_references",
    create_schema=OpenapiArtifactReferenceCreate,
    update_schema=OpenapiArtifactReferenceUpdate,
    response_schema=OpenapiArtifactReferenceResponse,
    default_sort="artifact_code",
    tag="DevPortal — OpenAPI Artifact",
)
register_lifecycle_route(
    openapi_artifact_references_router,
    path="/{row_id}/activate",
    resource="openapi_artifact_reference",
    action="activate",
    service_attr="openapi_artifact_references",
    method_name="activate",
    response_schema=OpenapiArtifactReferenceResponse,
    tag="DevPortal — OpenAPI Artifact",
    message="Activated",
)
register_lifecycle_route(
    openapi_artifact_references_router,
    path="/{row_id}/retire",
    resource="openapi_artifact_reference",
    action="retire",
    service_attr="openapi_artifact_references",
    method_name="retire",
    response_schema=OpenapiArtifactReferenceResponse,
    tag="DevPortal — OpenAPI Artifact",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    sandbox_environments_router,
    resource="sandbox_environment",
    service_attr="sandbox_environments",
    create_schema=SandboxEnvironmentCreate,
    update_schema=SandboxEnvironmentUpdate,
    response_schema=SandboxEnvironmentResponse,
    default_sort="environment_name",
    tag="DevPortal — Sandbox",
)
register_lifecycle_route(
    sandbox_environments_router,
    path="/{row_id}/activate",
    resource="sandbox_environment",
    action="activate",
    service_attr="sandbox_environments",
    method_name="activate",
    response_schema=SandboxEnvironmentResponse,
    tag="DevPortal — Sandbox",
    message="Activated",
)
register_lifecycle_route(
    sandbox_environments_router,
    path="/{row_id}/retire",
    resource="sandbox_environment",
    action="retire",
    service_attr="sandbox_environments",
    method_name="retire",
    response_schema=SandboxEnvironmentResponse,
    tag="DevPortal — Sandbox",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    tryit_sessions_router,
    resource="tryit_session",
    service_attr="tryit_sessions",
    create_schema=TryitSessionCreate,
    update_schema=TryitSessionUpdate,
    response_schema=TryitSessionResponse,
    default_sort="created_at",
    tag="DevPortal — Try-it",
)
register_lifecycle_route(
    tryit_sessions_router,
    path="/{row_id}/close",
    resource="tryit_session",
    action="close",
    service_attr="tryit_sessions",
    method_name="close",
    response_schema=TryitSessionResponse,
    tag="DevPortal — Try-it",
    message="Closed",
)
register_lifecycle_route(
    tryit_sessions_router,
    path="/{row_id}/expire",
    resource="tryit_session",
    action="expire",
    service_attr="tryit_sessions",
    method_name="expire",
    response_schema=TryitSessionResponse,
    tag="DevPortal — Try-it",
    message="Expired",
)
