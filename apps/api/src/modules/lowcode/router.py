"""Low-Code module router aggregation — Phase 1 · 2A · 2B · 2C · 3A · 3B · 4."""

from fastapi import APIRouter

from modules.lowcode.routers import (
    categories_router,
    component_versions_router,
    components_router,
    data_sources_router,
    definitions_router,
    event_handlers_router,
    expression_bindings_router,
    expressions_router,
    fields_router,
    localization_entries_router,
    page_definitions_router,
    page_regions_router,
    page_versions_router,
    preview_sessions_router,
    publish_history_router,
    runtime_submissions_router,
    sections_router,
    structure_router,
    versions_router,
)

lowcode_router = APIRouter(prefix="/lowcode")
lowcode_router.include_router(categories_router)
lowcode_router.include_router(definitions_router)
lowcode_router.include_router(versions_router)
lowcode_router.include_router(sections_router)
lowcode_router.include_router(fields_router)
lowcode_router.include_router(structure_router)
lowcode_router.include_router(components_router)
lowcode_router.include_router(component_versions_router)
lowcode_router.include_router(data_sources_router)
lowcode_router.include_router(expressions_router)
lowcode_router.include_router(expression_bindings_router)
lowcode_router.include_router(event_handlers_router)
lowcode_router.include_router(localization_entries_router)
lowcode_router.include_router(page_definitions_router)
lowcode_router.include_router(page_versions_router)
lowcode_router.include_router(page_regions_router)
lowcode_router.include_router(publish_history_router)
lowcode_router.include_router(runtime_submissions_router)
lowcode_router.include_router(preview_sessions_router)
