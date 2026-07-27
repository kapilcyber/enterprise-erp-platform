"""AI ops routers — usage, cost, cache."""

from fastapi import APIRouter

from modules.ai.routers._common import register_lifecycle_route, register_standard_crud
from modules.ai.schemas import (
    CacheEntryCreate,
    CacheEntryResponse,
    CacheEntryUpdate,
    CostRecordCreate,
    CostRecordResponse,
    CostRecordUpdate,
    LifecycleReason,
    UsageRecordCreate,
    UsageRecordResponse,
    UsageRecordUpdate,
)

usage_records_router = APIRouter(prefix="/usage-records", tags=["AI — Usage Record"])
cost_records_router = APIRouter(prefix="/cost-records", tags=["AI — Cost Record"])
cache_entries_router = APIRouter(prefix="/cache-entries", tags=["AI — Cache Entry"])

register_standard_crud(
    usage_records_router,
    resource="usage",
    service_attr="usage_records",
    create_schema=UsageRecordCreate,
    update_schema=UsageRecordUpdate,
    response_schema=UsageRecordResponse,
    default_sort="recorded_at",
    tag="AI — Usage Record",
)

register_standard_crud(
    cost_records_router,
    resource="cost",
    service_attr="cost_records",
    create_schema=CostRecordCreate,
    update_schema=CostRecordUpdate,
    response_schema=CostRecordResponse,
    default_sort="recorded_at",
    tag="AI — Cost Record",
)

register_standard_crud(
    cache_entries_router,
    resource="cache",
    service_attr="cache_entries",
    create_schema=CacheEntryCreate,
    update_schema=CacheEntryUpdate,
    response_schema=CacheEntryResponse,
    default_sort="cache_key",
    tag="AI — Cache Entry",
)
register_lifecycle_route(
    cache_entries_router,
    path="/{row_id}/invalidate",
    resource="cache",
    action="admin",
    service_attr="cache_entries",
    method_name="invalidate",
    response_schema=CacheEntryResponse,
    tag="AI — Cache Entry",
    message="Invalidated",
)
register_lifecycle_route(
    cache_entries_router,
    path="/{row_id}/expire",
    resource="cache",
    action="update",
    service_attr="cache_entries",
    method_name="expire",
    response_schema=CacheEntryResponse,
    tag="AI — Cache Entry",
    body_schema=LifecycleReason,
    message="Expired",
)
