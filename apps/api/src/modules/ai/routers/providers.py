"""AI registry routers — provider, model, credential, configuration."""

from fastapi import APIRouter

from modules.ai.routers._common import register_lifecycle_route, register_standard_crud
from modules.ai.schemas import (
    ConfigurationCreate,
    ConfigurationResponse,
    ConfigurationUpdate,
    CredentialCreate,
    CredentialResponse,
    CredentialRotate,
    CredentialUpdate,
    LifecycleReason,
    ModelCreate,
    ModelResponse,
    ModelUpdate,
    ProviderCreate,
    ProviderResponse,
    ProviderUpdate,
    RetireBody,
)

providers_router = APIRouter(prefix="/providers", tags=["AI — Provider"])
models_router = APIRouter(prefix="/models", tags=["AI — Model"])
credentials_router = APIRouter(prefix="/credentials", tags=["AI — Credential"])
configurations_router = APIRouter(prefix="/configurations", tags=["AI — Configuration"])

register_standard_crud(
    providers_router,
    resource="provider",
    service_attr="providers",
    create_schema=ProviderCreate,
    update_schema=ProviderUpdate,
    response_schema=ProviderResponse,
    default_sort="sort_order",
    tag="AI — Provider",
)
register_lifecycle_route(
    providers_router,
    path="/{row_id}/activate",
    resource="provider",
    action="update",
    service_attr="providers",
    method_name="activate",
    response_schema=ProviderResponse,
    tag="AI — Provider",
    message="Activated",
)
register_lifecycle_route(
    providers_router,
    path="/{row_id}/suspend",
    resource="provider",
    action="update",
    service_attr="providers",
    method_name="suspend",
    response_schema=ProviderResponse,
    tag="AI — Provider",
    message="Suspended",
)
register_lifecycle_route(
    providers_router,
    path="/{row_id}/retire",
    resource="provider",
    action="update",
    service_attr="providers",
    method_name="retire",
    response_schema=ProviderResponse,
    tag="AI — Provider",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    models_router,
    resource="model",
    service_attr="models",
    create_schema=ModelCreate,
    update_schema=ModelUpdate,
    response_schema=ModelResponse,
    default_sort="model_name",
    tag="AI — Model",
)
register_lifecycle_route(
    models_router,
    path="/{row_id}/approve",
    resource="model",
    action="update",
    service_attr="models",
    method_name="approve",
    response_schema=ModelResponse,
    tag="AI — Model",
    message="Approved",
)
register_lifecycle_route(
    models_router,
    path="/{row_id}/deprecate",
    resource="model",
    action="update",
    service_attr="models",
    method_name="deprecate",
    response_schema=ModelResponse,
    tag="AI — Model",
    message="Deprecated",
)
register_lifecycle_route(
    models_router,
    path="/{row_id}/retire",
    resource="model",
    action="update",
    service_attr="models",
    method_name="retire",
    response_schema=ModelResponse,
    tag="AI — Model",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    credentials_router,
    resource="credential",
    service_attr="credential_references",
    create_schema=CredentialCreate,
    update_schema=CredentialUpdate,
    response_schema=CredentialResponse,
    default_sort="credential_code",
    tag="AI — Credential",
)
register_lifecycle_route(
    credentials_router,
    path="/{row_id}/rotate",
    resource="credential",
    action="update",
    service_attr="credential_references",
    method_name="rotate",
    response_schema=CredentialResponse,
    tag="AI — Credential",
    body_schema=CredentialRotate,
    message="Rotated",
)
register_lifecycle_route(
    credentials_router,
    path="/{row_id}/retire",
    resource="credential",
    action="update",
    service_attr="credential_references",
    method_name="retire",
    response_schema=CredentialResponse,
    tag="AI — Credential",
    body_schema=RetireBody,
    message="Retired",
)

register_standard_crud(
    configurations_router,
    resource="configuration",
    service_attr="configurations",
    create_schema=ConfigurationCreate,
    update_schema=ConfigurationUpdate,
    response_schema=ConfigurationResponse,
    default_sort="config_name",
    tag="AI — Configuration",
)
register_lifecycle_route(
    configurations_router,
    path="/{row_id}/activate",
    resource="configuration",
    action="update",
    service_attr="configurations",
    method_name="activate",
    response_schema=ConfigurationResponse,
    tag="AI — Configuration",
    message="Activated",
)
register_lifecycle_route(
    configurations_router,
    path="/{row_id}/retire",
    resource="configuration",
    action="update",
    service_attr="configurations",
    method_name="retire",
    response_schema=ConfigurationResponse,
    tag="AI — Configuration",
    body_schema=RetireBody,
    message="Retired",
)
