"""API Developer Portal aggregate router — Phase 1–4."""

from fastapi import APIRouter

from modules.devportal.routers import (
    accounts_router,
    api_product_environments_router,
    api_product_versions_router,
    api_products_router,
    applications_router,
    documentation_entries_router,
    entitlements_router,
    invites_router,
    memberships_router,
    openapi_artifact_references_router,
    organizations_router,
    plans_router,
    reports_router,
    sandbox_environments_router,
    sessions_router,
    subscriptions_router,
    teams_router,
    tryit_sessions_router,
)

devportal_router = APIRouter(prefix="/devportal")
devportal_router.include_router(organizations_router)
devportal_router.include_router(teams_router)
devportal_router.include_router(accounts_router)
devportal_router.include_router(memberships_router)
devportal_router.include_router(invites_router)
devportal_router.include_router(sessions_router)
devportal_router.include_router(applications_router)
devportal_router.include_router(api_products_router)
devportal_router.include_router(api_product_versions_router)
devportal_router.include_router(api_product_environments_router)
devportal_router.include_router(plans_router)
devportal_router.include_router(subscriptions_router)
devportal_router.include_router(entitlements_router)
devportal_router.include_router(documentation_entries_router)
devportal_router.include_router(openapi_artifact_references_router)
devportal_router.include_router(sandbox_environments_router)
devportal_router.include_router(tryit_sessions_router)
devportal_router.include_router(reports_router)
