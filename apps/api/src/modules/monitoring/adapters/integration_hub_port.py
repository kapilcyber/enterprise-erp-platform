"""Integration Hub projection port — consume-only (Phase 0).

Monitoring never writes Hub ORM models. Optional health/transport projection via contracts.
"""

from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class MonitoringIntegrationHubAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_binding_ref(self, ctx: TenantContext, binding_id: UUID | None) -> UUID | None:
        """Pass-through Hub binding UUID — no Hub ORM load."""
        _ = (ctx, self._db)
        return binding_id

    def project_transport_health(
        self,
        ctx: TenantContext,
        *,
        filters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Contract projection stub — fail closed; Hub remains transport SoR."""
        _ = (ctx, self._db)
        return {
            "source": "integration_hub",
            "filters": filters or {},
            "projected": True,
            "status": "unknown",
            "note": "Metadata projection only — Integration Hub owns transport",
        }
