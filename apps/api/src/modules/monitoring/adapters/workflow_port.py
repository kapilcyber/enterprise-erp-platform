"""Foundation Workflow port — consume-only (Phase 0).

Monitoring initiates / participates; Foundation Workflow Engine remains SoR (C-04).
"""

from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class MonitoringWorkflowAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_workflow_instance_ref(
        self, ctx: TenantContext, workflow_instance_id: UUID | None
    ) -> UUID | None:
        """Pass-through workflow instance UUID — Foundation executes workflow."""
        _ = (ctx, self._db)
        return workflow_instance_id
