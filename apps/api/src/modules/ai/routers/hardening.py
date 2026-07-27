"""AI hardening routers — Phase 4 evaluation, feedback, multimodal (NO runtime execution)."""

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
    EvaluationCompleteBody,
    EvaluationCreate,
    EvaluationFailBody,
    EvaluationResponse,
    EvaluationUpdate,
    FeedbackCreate,
    FeedbackResponse,
    FeedbackUpdate,
    MultimodalProfileCreate,
    MultimodalProfileResponse,
    MultimodalProfileUpdate,
    PublishBody,
    RetireBody,
)
from modules.foundation.domain.value_objects import TenantContext
from shared.schemas import APIResponse

evaluations_router = APIRouter(prefix="/evaluations", tags=["AI — Evaluation"])
feedbacks_router = APIRouter(prefix="/feedbacks", tags=["AI — Feedback"])
multimodal_profiles_router = APIRouter(
    prefix="/multimodal-profiles", tags=["AI — Multimodal Profile"]
)

register_standard_crud(
    evaluations_router,
    resource="evaluation",
    service_attr="evaluations",
    create_schema=EvaluationCreate,
    update_schema=EvaluationUpdate,
    response_schema=EvaluationResponse,
    default_sort="queued_at",
    tag="AI — Evaluation",
)
register_lifecycle_route(
    evaluations_router,
    path="/{row_id}/start",
    resource="evaluation",
    action="start",
    service_attr="evaluations",
    method_name="start",
    response_schema=EvaluationResponse,
    tag="AI — Evaluation",
    message="Started",
)

register_standard_crud(
    feedbacks_router,
    resource="feedback",
    service_attr="feedbacks",
    create_schema=FeedbackCreate,
    update_schema=FeedbackUpdate,
    response_schema=FeedbackResponse,
    default_sort="created_at",
    tag="AI — Feedback",
)
register_lifecycle_route(
    feedbacks_router,
    path="/{row_id}/review",
    resource="feedback",
    action="review",
    service_attr="feedbacks",
    method_name="review",
    response_schema=FeedbackResponse,
    tag="AI — Feedback",
    message="Reviewed",
)
register_lifecycle_route(
    feedbacks_router,
    path="/{row_id}/close",
    resource="feedback",
    action="close",
    service_attr="feedbacks",
    method_name="close",
    response_schema=FeedbackResponse,
    tag="AI — Feedback",
    message="Closed",
)

register_standard_crud(
    multimodal_profiles_router,
    resource="multimodal_profile",
    service_attr="multimodal_profiles",
    create_schema=MultimodalProfileCreate,
    update_schema=MultimodalProfileUpdate,
    response_schema=MultimodalProfileResponse,
    default_sort="profile_name",
    tag="AI — Multimodal Profile",
)
register_lifecycle_route(
    multimodal_profiles_router,
    path="/{row_id}/publish",
    resource="multimodal_profile",
    action="publish",
    service_attr="multimodal_profiles",
    method_name="publish",
    response_schema=MultimodalProfileResponse,
    tag="AI — Multimodal Profile",
    body_schema=PublishBody,
    message="Published",
)
register_lifecycle_route(
    multimodal_profiles_router,
    path="/{row_id}/retire",
    resource="multimodal_profile",
    action="retire",
    service_attr="multimodal_profiles",
    method_name="retire",
    response_schema=MultimodalProfileResponse,
    tag="AI — Multimodal Profile",
    body_schema=RetireBody,
    message="Retired",
)


@evaluations_router.post(
    "/{row_id}/complete",
    response_model=APIResponse[EvaluationResponse],
    tags=["AI — Evaluation"],
)
def complete_evaluation(
    row_id: UUID,
    body: EvaluationCompleteBody,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.evaluation:complete"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Completed",
        data=_app(db).evaluations.complete(
            ctx,
            row_id,
            result_summary_json=body.result_summary_json,
            metrics_json=body.metrics_json,
        ),
    )


@evaluations_router.post(
    "/{row_id}/fail",
    response_model=APIResponse[EvaluationResponse],
    tags=["AI — Evaluation"],
)
def fail_evaluation(
    row_id: UUID,
    body: EvaluationFailBody,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.evaluation:fail"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="Failed",
        data=_app(db).evaluations.fail(ctx, row_id, failure_reason=body.failure_reason),
    )


@evaluations_router.get(
    "/{row_id}/result-summary",
    response_model=APIResponse[dict[str, Any]],
    tags=["AI — Evaluation"],
)
def get_evaluation_result_summary(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.evaluation:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK",
        data=_app(db).evaluations.get_result_summary(ctx, row_id),
    )


@multimodal_profiles_router.get(
    "/{row_id}/readiness",
    response_model=APIResponse[dict[str, Any]],
    tags=["AI — Multimodal Profile"],
)
def get_multimodal_readiness(
    row_id: UUID,
    ctx: Annotated[TenantContext, Depends(require_permission("ai.multimodal_profile:read"))],
    db: Annotated[Session, Depends(get_db)],
):
    return APIResponse(
        message="OK",
        data=_app(db).multimodal_profiles.get_readiness_snapshot(ctx, row_id),
    )
