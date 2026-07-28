"""Shared Developer Portal router utilities — thin handler helpers."""

from collections.abc import Callable
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.devportal.dependencies import (
    PaginationParams,
    SortParams,
    extract_update_fields,
    get_db,
    get_pagination,
    get_sort,
    page_payload,
    require_permission,
)
from modules.devportal.service.application_service import DevportalApplicationService
from modules.foundation.domain.value_objects import TenantContext
from shared.schemas import APIResponse


def _app(db: Session) -> DevportalApplicationService:
    return DevportalApplicationService(db)


def register_standard_crud(
    router: APIRouter,
    *,
    resource: str,
    service_attr: str,
    create_schema: type,
    update_schema: type,
    response_schema: type,
    default_sort: str,
    tag: str,
    create_handler: Callable | None = None,
) -> None:
    """Register list/get/create/patch/archive/restore routes on *router*."""

    read_perm = f"devportal.{resource}:read"
    create_perm = f"devportal.{resource}:create"
    update_perm = f"devportal.{resource}:update"
    archive_perm = f"devportal.{resource}:archive"
    restore_perm = f"devportal.{resource}:restore"
    response_model: Any = APIResponse[response_schema]  # type: ignore[valid-type]

    @router.get("", response_model=APIResponse[dict[str, Any]], tags=[tag])
    def list_rows(
        ctx: Annotated[TenantContext, Depends(require_permission(read_perm))],
        db: Annotated[Session, Depends(get_db)],
        pagination: Annotated[PaginationParams, Depends(get_pagination)],
        sort: Annotated[SortParams, Depends(get_sort)],
        company_id: UUID | None = None,
        status: str | None = None,
        search: str | None = None,
    ):
        svc = getattr(_app(db), service_attr)
        page = svc.list(
            ctx,
            company_id=company_id,
            status=status,
            search=search,
            page=pagination.page,
            page_size=pagination.page_size,
            sort_by=sort.sort_by or default_sort,
            sort_dir=sort.sort_dir,
        )
        return APIResponse(message="OK", data=page_payload(page))

    @router.get("/{row_id}", response_model=response_model, tags=[tag])
    def get_row(
        row_id: UUID,
        ctx: Annotated[TenantContext, Depends(require_permission(read_perm))],
        db: Annotated[Session, Depends(get_db)],
    ):
        svc = getattr(_app(db), service_attr)
        return APIResponse(message="OK", data=svc.get(ctx, row_id))

    if create_handler is not None:

        @router.post("", response_model=response_model, tags=[tag])
        def create_row(
            body: create_schema,  # type: ignore[valid-type]
            ctx: Annotated[TenantContext, Depends(require_permission(create_perm))],
            db: Annotated[Session, Depends(get_db)],
        ):
            return create_handler(ctx, db, body)

    else:

        @router.post("", response_model=response_model, tags=[tag])
        def create_row(
            body: create_schema,  # type: ignore[valid-type]
            ctx: Annotated[TenantContext, Depends(require_permission(create_perm))],
            db: Annotated[Session, Depends(get_db)],
        ):
            svc = getattr(_app(db), service_attr)
            return APIResponse(
                message="Created",
                data=svc.create(ctx, **body.model_dump(exclude_none=True)),
            )

    @router.patch("/{row_id}", response_model=response_model, tags=[tag])
    def update_row(
        row_id: UUID,
        body: update_schema,  # type: ignore[valid-type]
        ctx: Annotated[TenantContext, Depends(require_permission(update_perm))],
        db: Annotated[Session, Depends(get_db)],
    ):
        svc = getattr(_app(db), service_attr)
        return APIResponse(
            message="Updated",
            data=svc.update(ctx, row_id, **extract_update_fields(body)),
        )

    @router.post("/{row_id}/archive", response_model=response_model, tags=[tag])
    def archive_row(
        row_id: UUID,
        ctx: Annotated[TenantContext, Depends(require_permission(archive_perm))],
        db: Annotated[Session, Depends(get_db)],
    ):
        svc = getattr(_app(db), service_attr)
        return APIResponse(message="Archived", data=svc.archive(ctx, row_id))

    @router.post("/{row_id}/restore", response_model=response_model, tags=[tag])
    def restore_row(
        row_id: UUID,
        ctx: Annotated[TenantContext, Depends(require_permission(restore_perm))],
        db: Annotated[Session, Depends(get_db)],
    ):
        svc = getattr(_app(db), service_attr)
        return APIResponse(message="Restored", data=svc.restore(ctx, row_id))


def register_lifecycle_route(
    router: APIRouter,
    *,
    path: str,
    resource: str,
    action: str,
    service_attr: str,
    method_name: str,
    response_schema: type,
    tag: str,
    body_schema: type | None = None,
    message: str | None = None,
) -> None:
    """Register a single POST lifecycle route."""

    perm = f"devportal.{resource}:{action}"
    response_message = message or action.replace("-", " ").title()
    response_model: Any = APIResponse[response_schema]  # type: ignore[valid-type]

    if body_schema is None:

        @router.post(path, response_model=response_model, tags=[tag])
        def lifecycle_handler(
            row_id: UUID,
            ctx: Annotated[TenantContext, Depends(require_permission(perm))],
            db: Annotated[Session, Depends(get_db)],
        ):
            svc = getattr(_app(db), service_attr)
            return APIResponse(
                message=response_message,
                data=getattr(svc, method_name)(ctx, row_id),
            )

    else:

        @router.post(path, response_model=response_model, tags=[tag])
        def lifecycle_handler_with_body(
            row_id: UUID,
            body: body_schema,  # type: ignore[valid-type]
            ctx: Annotated[TenantContext, Depends(require_permission(perm))],
            db: Annotated[Session, Depends(get_db)],
        ):
            svc = getattr(_app(db), service_attr)
            kwargs = body.model_dump(exclude_none=True)
            return APIResponse(
                message=response_message,
                data=getattr(svc, method_name)(ctx, row_id, **kwargs),
            )
