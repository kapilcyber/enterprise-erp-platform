"""Foundation Security / Workflow port — consume-only (Phase 1).

Developer Portal never writes Foundation ORM models. Cross-module reads/writes
use service contracts and UUID references only (Architecture Lock / no peer ORM).
"""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class DevportalFoundationAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_role_ref(self, ctx: TenantContext, role_id: UUID | None) -> UUID | None:
        """Pass-through UUID role reference — no peer ORM load."""
        _ = (ctx, self._db)
        return role_id

    def resolve_user_ref(self, ctx: TenantContext, user_id: UUID | None) -> UUID | None:
        """Pass-through Foundation user UUID — Auth SoR remains Foundation."""
        _ = (ctx, self._db)
        return user_id

    def resolve_workflow_instance_ref(
        self, ctx: TenantContext, workflow_instance_id: UUID | None
    ) -> UUID | None:
        """Pass-through workflow instance UUID — Foundation executes workflow."""
        _ = (ctx, self._db)
        return workflow_instance_id
