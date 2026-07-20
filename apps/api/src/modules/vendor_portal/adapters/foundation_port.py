"""Foundation port — workflow / audit / notification refs."""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class VendorPortalFoundationAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_workflow_instance(self, ctx: TenantContext, instance_id: UUID | None) -> UUID | None:  # noqa: E501
        _ = (ctx, self._db)
        return instance_id
