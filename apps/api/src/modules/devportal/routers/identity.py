"""Developer Portal Phase 1 identity routers."""

from fastapi import APIRouter

from modules.devportal.routers._common import register_lifecycle_route, register_standard_crud
from modules.devportal.schemas import (
    DeveloperAccountCreate,
    DeveloperAccountResponse,
    DeveloperAccountUpdate,
    DeveloperInviteCreate,
    DeveloperInviteResponse,
    DeveloperInviteUpdate,
    DeveloperMembershipCreate,
    DeveloperMembershipResponse,
    DeveloperMembershipUpdate,
    DeveloperOrganizationCreate,
    DeveloperOrganizationResponse,
    DeveloperOrganizationUpdate,
    DeveloperTeamCreate,
    DeveloperTeamResponse,
    DeveloperTeamUpdate,
    LifecycleReason,
    PortalSessionCreate,
    PortalSessionResponse,
    PortalSessionUpdate,
)

organizations_router = APIRouter(prefix="/organizations", tags=["DevPortal — Organization"])
teams_router = APIRouter(prefix="/teams", tags=["DevPortal — Team"])
accounts_router = APIRouter(prefix="/accounts", tags=["DevPortal — Account"])
memberships_router = APIRouter(prefix="/memberships", tags=["DevPortal — Membership"])
invites_router = APIRouter(prefix="/invites", tags=["DevPortal — Invite"])
sessions_router = APIRouter(prefix="/sessions", tags=["DevPortal — Session"])

register_standard_crud(
    organizations_router,
    resource="developer_organization",
    service_attr="organizations",
    create_schema=DeveloperOrganizationCreate,
    update_schema=DeveloperOrganizationUpdate,
    response_schema=DeveloperOrganizationResponse,
    default_sort="org_name",
    tag="DevPortal — Organization",
)

register_standard_crud(
    teams_router,
    resource="developer_team",
    service_attr="teams",
    create_schema=DeveloperTeamCreate,
    update_schema=DeveloperTeamUpdate,
    response_schema=DeveloperTeamResponse,
    default_sort="team_name",
    tag="DevPortal — Team",
)

register_standard_crud(
    accounts_router,
    resource="developer_account",
    service_attr="accounts",
    create_schema=DeveloperAccountCreate,
    update_schema=DeveloperAccountUpdate,
    response_schema=DeveloperAccountResponse,
    default_sort="display_name",
    tag="DevPortal — Account",
)
for path, action, method, msg in (
    ("/{row_id}/submit", "submit", "submit", "Submitted"),
    ("/{row_id}/approve", "approve", "approve", "Approved"),
    ("/{row_id}/activate", "activate", "activate", "Activated"),
    ("/{row_id}/lock", "lock", "lock", "Locked"),
    ("/{row_id}/suspend", "suspend", "suspend", "Suspended"),
):
    register_lifecycle_route(
        accounts_router,
        path=path,
        resource="developer_account",
        action=action,
        service_attr="accounts",
        method_name=method,
        response_schema=DeveloperAccountResponse,
        tag="DevPortal — Account",
        message=msg,
    )
register_lifecycle_route(
    accounts_router,
    path="/{row_id}/retire",
    resource="developer_account",
    action="retire",
    service_attr="accounts",
    method_name="retire",
    response_schema=DeveloperAccountResponse,
    tag="DevPortal — Account",
    body_schema=LifecycleReason,
    message="Retired",
)

register_standard_crud(
    memberships_router,
    resource="developer_membership",
    service_attr="memberships",
    create_schema=DeveloperMembershipCreate,
    update_schema=DeveloperMembershipUpdate,
    response_schema=DeveloperMembershipResponse,
    default_sort="created_at",
    tag="DevPortal — Membership",
)

register_standard_crud(
    invites_router,
    resource="developer_invite",
    service_attr="invites",
    create_schema=DeveloperInviteCreate,
    update_schema=DeveloperInviteUpdate,
    response_schema=DeveloperInviteResponse,
    default_sort="created_at",
    tag="DevPortal — Invite",
)
for path, action, method, msg in (
    ("/{row_id}/submit", "submit", "submit", "Submitted"),
    ("/{row_id}/approve", "approve", "approve", "Approved"),
    ("/{row_id}/send", "send", "mark_sent", "Sent"),
    ("/{row_id}/accept", "accept", "accept", "Accepted"),
    ("/{row_id}/expire", "expire", "expire", "Expired"),
    ("/{row_id}/revoke", "revoke", "revoke", "Revoked"),
):
    register_lifecycle_route(
        invites_router,
        path=path,
        resource="developer_invite",
        action=action,
        service_attr="invites",
        method_name=method,
        response_schema=DeveloperInviteResponse,
        tag="DevPortal — Invite",
        message=msg,
    )

register_standard_crud(
    sessions_router,
    resource="portal_session",
    service_attr="sessions",
    create_schema=PortalSessionCreate,
    update_schema=PortalSessionUpdate,
    response_schema=PortalSessionResponse,
    default_sort="created_at",
    tag="DevPortal — Session",
)
register_lifecycle_route(
    sessions_router,
    path="/{row_id}/expire",
    resource="portal_session",
    action="expire",
    service_attr="sessions",
    method_name="expire",
    response_schema=PortalSessionResponse,
    tag="DevPortal — Session",
    message="Expired",
)
register_lifecycle_route(
    sessions_router,
    path="/{row_id}/revoke",
    resource="portal_session",
    action="revoke",
    service_attr="sessions",
    method_name="revoke",
    response_schema=PortalSessionResponse,
    tag="DevPortal — Session",
    message="Revoked",
)
