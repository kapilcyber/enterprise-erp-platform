"""External observability platform port — Phase 0 skeleton.

External platforms (Prometheus / Grafana / Loki / OTel / cloud APM / SIEM) remain external.
secret_ref only — never materialize secrets. Fail closed — never invent healthy binding state.
"""

from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class MonitoringExternalPlatformAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_secret_ref(self, ctx: TenantContext, secret_ref: UUID | None) -> UUID | None:
        """Pass-through secret reference UUID — never load plaintext secrets."""
        _ = (ctx, self._db)
        return secret_ref

    def validate_binding(
        self,
        ctx: TenantContext,
        *,
        platform_type: str,
        secret_ref: UUID | None,
        endpoint_ref: str | None = None,
    ) -> dict[str, Any]:
        """Binding validation stub — platforms remain external; fail closed."""
        _ = (ctx, self._db, endpoint_ref)
        return {
            "platform_type": platform_type,
            "secret_ref": str(secret_ref) if secret_ref else None,
            "validated": False,
            "status": "unknown",
            "note": "External platform remains SoR — Monitoring stores binding metadata only",
        }
