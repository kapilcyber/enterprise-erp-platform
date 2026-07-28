"""Publish validation for API product versions — Phase 1."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.devportal.domain.value_objects import PublishValidationResult
from modules.devportal.repository.api_product_version_repository import (
    ApiProductVersionRepository,
)
from modules.devportal.service.engines import PublishGateEngine
from modules.foundation.domain.value_objects import TenantContext


class PublishValidationService:
    def __init__(self, db: Session) -> None:
        self._repo = ApiProductVersionRepository(db)
        self._gate = PublishGateEngine()

    def validate_product_version(self, ctx: TenantContext, row_id: UUID) -> PublishValidationResult:
        row = self._repo.get(ctx, row_id)
        if row is None:
            raise NotFoundException("ApiProductVersion not found")
        issues = self._gate.validate_draft_for_publish(row)
        return PublishValidationResult(
            valid=len(issues) == 0,
            version_id=row.id,
            product_id=row.product_id,
            issues=issues,
        )
