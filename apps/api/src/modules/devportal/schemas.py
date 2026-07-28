"""API Developer Portal Pydantic schemas — Phase 1."""

from datetime import date, datetime
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PageMeta(BaseModel):
    total: int
    page: int
    page_size: int
    sort_by: str | None = None
    sort_dir: str = "asc"


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    sort_by: str | None = None
    sort_dir: str = "asc"


def page_of(
    items: list[T],
    *,
    total: int,
    page: int,
    page_size: int,
    sort_by: str | None = None,
    sort_dir: str = "asc",
) -> Page[T]:
    return Page(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )


class MessageResponse(BaseModel):
    message: str


class LifecycleReason(BaseModel):
    reason: str | None = None


class ValidationIssueResponse(BaseModel):
    code: str
    message: str
    severity: str = "error"
    field: str | None = None


class PublishValidationResponse(BaseModel):
    valid: bool
    version_id: UUID
    product_id: UUID
    issues: list[ValidationIssueResponse] = Field(default_factory=list)
    warnings: list[ValidationIssueResponse] = Field(default_factory=list)


# --- Developer Organization ---


class DeveloperOrganizationCreate(BaseModel):
    company_id: UUID | None = None
    org_code: str | None = None
    org_name: str
    description: str | None = None
    status: str | None = "active"
    sort_order: int | None = 0


class DeveloperOrganizationUpdate(BaseModel):
    org_name: str | None = None
    description: str | None = None
    sort_order: int | None = None
    version: int | None = None


class DeveloperOrganizationResponse(OrmModel):
    id: UUID
    company_id: UUID
    org_code: str
    org_name: str
    description: str | None = None
    status: str
    sort_order: int
    version: int
    is_deleted: bool | None = None


# --- Developer Team ---


class DeveloperTeamCreate(BaseModel):
    company_id: UUID | None = None
    organization_id: UUID
    team_code: str | None = None
    team_name: str
    description: str | None = None
    status: str | None = "active"
    sort_order: int | None = 0


class DeveloperTeamUpdate(BaseModel):
    team_name: str | None = None
    description: str | None = None
    sort_order: int | None = None
    version: int | None = None


class DeveloperTeamResponse(OrmModel):
    id: UUID
    company_id: UUID
    organization_id: UUID
    team_code: str
    team_name: str
    description: str | None = None
    status: str
    sort_order: int
    version: int
    is_deleted: bool | None = None


# --- Developer Account ---


class DeveloperAccountCreate(BaseModel):
    company_id: UUID | None = None
    account_code: str | None = None
    display_name: str
    email: str
    foundation_user_id: UUID | None = None
    status: str | None = "draft"


class DeveloperAccountUpdate(BaseModel):
    display_name: str | None = None
    email: str | None = None
    foundation_user_id: UUID | None = None
    version: int | None = None


class DeveloperAccountResponse(OrmModel):
    id: UUID
    company_id: UUID
    account_code: str
    display_name: str
    email: str
    foundation_user_id: UUID | None = None
    status: str
    workflow_status: str | None = None
    workflow_instance_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Developer Membership ---


class DeveloperMembershipCreate(BaseModel):
    company_id: UUID | None = None
    account_id: UUID
    organization_id: UUID
    team_id: UUID | None = None
    membership_role: str | None = "member"
    status: str | None = "active"


class DeveloperMembershipUpdate(BaseModel):
    team_id: UUID | None = None
    membership_role: str | None = None
    version: int | None = None


class DeveloperMembershipResponse(OrmModel):
    id: UUID
    company_id: UUID
    account_id: UUID
    organization_id: UUID
    team_id: UUID | None = None
    membership_role: str
    status: str
    version: int
    is_deleted: bool | None = None


# --- Developer Invite ---


class DeveloperInviteCreate(BaseModel):
    company_id: UUID | None = None
    invite_code: str | None = None
    invite_email: str
    organization_id: UUID
    team_id: UUID | None = None
    account_id: UUID | None = None
    status: str | None = "draft"
    workflow_instance_id: UUID | None = None


class DeveloperInviteUpdate(BaseModel):
    invite_email: str | None = None
    team_id: UUID | None = None
    account_id: UUID | None = None
    workflow_instance_id: UUID | None = None
    version: int | None = None


class DeveloperInviteResponse(OrmModel):
    id: UUID
    company_id: UUID
    invite_code: str
    invite_email: str
    organization_id: UUID
    team_id: UUID | None = None
    account_id: UUID | None = None
    status: str
    workflow_status: str | None = None
    workflow_instance_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Portal Session ---


class PortalSessionCreate(BaseModel):
    company_id: UUID | None = None
    account_id: UUID
    session_ref: str | None = None
    status: str | None = "active"
    started_at: datetime | None = None
    expires_at: datetime | None = None


class PortalSessionUpdate(BaseModel):
    expires_at: datetime | None = None
    version: int | None = None


class PortalSessionResponse(OrmModel):
    id: UUID
    company_id: UUID
    account_id: UUID
    session_ref: str
    status: str
    started_at: datetime | None = None
    expires_at: datetime | None = None
    version: int
    is_deleted: bool | None = None


# --- Application ---


class ApplicationCreate(BaseModel):
    company_id: UUID | None = None
    account_id: UUID
    organization_id: UUID | None = None
    application_code: str | None = None
    application_name: str
    description: str | None = None
    oauth_client_id: UUID | None = None
    api_credential_id: UUID | None = None
    status: str | None = "draft"
    workflow_instance_id: UUID | None = None


class ApplicationUpdate(BaseModel):
    application_name: str | None = None
    description: str | None = None
    organization_id: UUID | None = None
    workflow_instance_id: UUID | None = None
    version: int | None = None


class ApplicationBindHub(BaseModel):
    oauth_client_id: UUID | None = None
    api_credential_id: UUID | None = None


class ApplicationResponse(OrmModel):
    id: UUID
    company_id: UUID
    account_id: UUID
    organization_id: UUID | None = None
    application_code: str
    application_name: str
    description: str | None = None
    oauth_client_id: UUID | None = None
    api_credential_id: UUID | None = None
    status: str
    workflow_status: str | None = None
    workflow_instance_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- API Product ---


class ApiProductCreate(BaseModel):
    company_id: UUID | None = None
    product_code: str | None = None
    product_name: str
    description: str | None = None
    status: str | None = "active"
    sort_order: int | None = 0


class ApiProductUpdate(BaseModel):
    product_name: str | None = None
    description: str | None = None
    sort_order: int | None = None
    version: int | None = None


class ApiProductResponse(OrmModel):
    id: UUID
    company_id: UUID
    product_code: str
    product_name: str
    description: str | None = None
    status: str
    sort_order: int
    version: int
    is_deleted: bool | None = None


# --- API Product Version ---


class ApiProductVersionCreate(BaseModel):
    company_id: UUID | None = None
    product_id: UUID
    version_label: str
    changelog_summary: str | None = None
    status: str | None = "draft"


class ApiProductVersionUpdate(BaseModel):
    version_label: str | None = None
    changelog_summary: str | None = None
    version: int | None = None


class ApiProductVersionResponse(OrmModel):
    id: UUID
    company_id: UUID
    product_id: UUID
    version_label: str
    changelog_summary: str | None = None
    status: str
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- API Product Environment ---


class ApiProductEnvironmentCreate(BaseModel):
    company_id: UUID | None = None
    product_version_id: UUID
    environment_code: str
    environment_name: str
    base_url_hint: str | None = None
    description: str | None = None
    status: str | None = "active"


class ApiProductEnvironmentUpdate(BaseModel):
    environment_name: str | None = None
    base_url_hint: str | None = None
    description: str | None = None
    version: int | None = None


class ApiProductEnvironmentResponse(OrmModel):
    id: UUID
    company_id: UUID
    product_version_id: UUID
    environment_code: str
    environment_name: str
    base_url_hint: str | None = None
    description: str | None = None
    status: str
    version: int
    is_deleted: bool | None = None


# --- Plan ---


class PlanCreate(BaseModel):
    company_id: UUID | None = None
    plan_code: str | None = None
    plan_name: str
    description: str | None = None
    status: str | None = "draft"
    sort_order: int | None = 0


class PlanUpdate(BaseModel):
    plan_name: str | None = None
    description: str | None = None
    sort_order: int | None = None
    version: int | None = None


class PlanResponse(OrmModel):
    id: UUID
    company_id: UUID
    plan_code: str
    plan_name: str
    description: str | None = None
    status: str
    sort_order: int
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Subscription ---


class SubscriptionCreate(BaseModel):
    company_id: UUID | None = None
    subscription_code: str | None = None
    application_id: UUID
    product_version_id: UUID
    plan_id: UUID
    description: str | None = None
    status: str | None = "draft"
    workflow_instance_id: UUID | None = None


class SubscriptionUpdate(BaseModel):
    description: str | None = None
    application_id: UUID | None = None
    product_version_id: UUID | None = None
    plan_id: UUID | None = None
    workflow_instance_id: UUID | None = None
    version: int | None = None


class SubscriptionResponse(OrmModel):
    id: UUID
    company_id: UUID
    subscription_code: str
    application_id: UUID
    product_version_id: UUID
    plan_id: UUID
    description: str | None = None
    status: str
    workflow_status: str | None = None
    workflow_instance_id: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- Entitlement ---


class EntitlementCreate(BaseModel):
    company_id: UUID | None = None
    subscription_id: UUID
    scope_code: str
    scope_name: str
    description: str | None = None
    status: str | None = "active"


class EntitlementUpdate(BaseModel):
    scope_name: str | None = None
    description: str | None = None
    version: int | None = None


class EntitlementResponse(OrmModel):
    id: UUID
    company_id: UUID
    subscription_id: UUID
    scope_code: str
    scope_name: str
    description: str | None = None
    status: str
    version: int
    is_deleted: bool | None = None


# --- Documentation Entry ---


class DocumentationEntryCreate(BaseModel):
    company_id: UUID | None = None
    product_version_id: UUID
    entry_code: str | None = None
    title: str
    entry_type: str
    summary: str | None = None
    status: str | None = "draft"


class DocumentationEntryUpdate(BaseModel):
    title: str | None = None
    entry_type: str | None = None
    summary: str | None = None
    version: int | None = None


class DocumentationEntryResponse(OrmModel):
    id: UUID
    company_id: UUID
    product_version_id: UUID
    entry_code: str
    title: str
    entry_type: str
    summary: str | None = None
    status: str
    published_at: datetime | None = None
    published_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    version: int
    is_deleted: bool | None = None


# --- OpenAPI Artifact Reference ---


class OpenapiArtifactReferenceCreate(BaseModel):
    company_id: UUID | None = None
    product_version_id: UUID
    documentation_entry_id: UUID | None = None
    artifact_code: str | None = None
    document_id: UUID
    openapi_version: str | None = None
    snapshot_label: str | None = None
    snapshot_notes: str | None = None
    status: str | None = "active"


class OpenapiArtifactReferenceUpdate(BaseModel):
    documentation_entry_id: UUID | None = None
    document_id: UUID | None = None
    openapi_version: str | None = None
    snapshot_label: str | None = None
    snapshot_notes: str | None = None
    version: int | None = None


class OpenapiArtifactReferenceResponse(OrmModel):
    id: UUID
    company_id: UUID
    product_version_id: UUID
    documentation_entry_id: UUID | None = None
    artifact_code: str
    document_id: UUID
    openapi_version: str | None = None
    snapshot_label: str | None = None
    snapshot_notes: str | None = None
    status: str
    version: int
    is_deleted: bool | None = None


# --- Sandbox Environment ---


class SandboxEnvironmentCreate(BaseModel):
    company_id: UUID | None = None
    environment_code: str | None = None
    environment_name: str
    description: str | None = None
    base_url_hint: str | None = None
    status: str | None = "draft"


class SandboxEnvironmentUpdate(BaseModel):
    environment_name: str | None = None
    description: str | None = None
    base_url_hint: str | None = None
    version: int | None = None


class SandboxEnvironmentResponse(OrmModel):
    id: UUID
    company_id: UUID
    environment_code: str
    environment_name: str
    description: str | None = None
    base_url_hint: str | None = None
    status: str
    version: int
    is_deleted: bool | None = None


# --- Try-it Session ---


class TryitSessionCreate(BaseModel):
    company_id: UUID | None = None
    session_code: str | None = None
    sandbox_environment_id: UUID
    application_id: UUID | None = None
    product_version_id: UUID | None = None
    status: str | None = "active"
    started_at: datetime | None = None
    expires_at: datetime | None = None


class TryitSessionUpdate(BaseModel):
    application_id: UUID | None = None
    product_version_id: UUID | None = None
    expires_at: datetime | None = None
    version: int | None = None


class TryitSessionResponse(OrmModel):
    id: UUID
    company_id: UUID
    session_code: str
    sandbox_environment_id: UUID
    application_id: UUID | None = None
    product_version_id: UUID | None = None
    status: str
    started_at: datetime | None = None
    closed_at: datetime | None = None
    expires_at: datetime | None = None
    version: int
    is_deleted: bool | None = None


# --- Portal Report (Phase 4) ---


class PortalReportCreate(BaseModel):
    company_id: UUID | None = None
    report_code: str | None = None
    report_name: str
    report_type: str
    description: str | None = None
    filters_json: dict | None = None
    config_json: dict | None = None
    export_preferences_json: dict | None = None
    schedule_metadata_json: dict | None = None
    period_start: date | None = None
    period_end: date | None = None
    analytics_report_id: UUID | None = None
    status: str | None = "draft"


class PortalReportUpdate(BaseModel):
    report_name: str | None = None
    report_type: str | None = None
    description: str | None = None
    filters_json: dict | None = None
    config_json: dict | None = None
    export_preferences_json: dict | None = None
    schedule_metadata_json: dict | None = None
    period_start: date | None = None
    period_end: date | None = None
    analytics_report_id: UUID | None = None
    version: int | None = None


class PortalReportResponse(OrmModel):
    id: UUID
    company_id: UUID
    report_code: str
    report_name: str
    report_type: str
    description: str | None = None
    filters_json: dict | None = None
    config_json: dict | None = None
    export_preferences_json: dict | None = None
    schedule_metadata_json: dict | None = None
    period_start: date | None = None
    period_end: date | None = None
    projection_snapshot_json: dict | None = None
    projected_at: datetime | None = None
    analytics_report_id: UUID | None = None
    status: str
    finalized_at: datetime | None = None
    finalized_by: UUID | None = None
    retired_at: datetime | None = None
    retired_by: UUID | None = None
    version: int
    is_deleted: bool | None = None
