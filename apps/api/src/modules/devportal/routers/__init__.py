"""API Developer Portal routers — Phase 1–4."""

from modules.devportal.routers.access import (
    entitlements_router,
    plans_router,
    subscriptions_router,
)
from modules.devportal.routers.catalog import (
    api_product_environments_router,
    api_product_versions_router,
    api_products_router,
    applications_router,
)
from modules.devportal.routers.experience import (
    documentation_entries_router,
    openapi_artifact_references_router,
    sandbox_environments_router,
    tryit_sessions_router,
)
from modules.devportal.routers.identity import (
    accounts_router,
    invites_router,
    memberships_router,
    organizations_router,
    sessions_router,
    teams_router,
)
from modules.devportal.routers.operations import reports_router

__all__ = [
    "accounts_router",
    "api_product_environments_router",
    "api_product_versions_router",
    "api_products_router",
    "applications_router",
    "documentation_entries_router",
    "entitlements_router",
    "invites_router",
    "memberships_router",
    "openapi_artifact_references_router",
    "organizations_router",
    "plans_router",
    "reports_router",
    "sandbox_environments_router",
    "sessions_router",
    "subscriptions_router",
    "teams_router",
    "tryit_sessions_router",
]
