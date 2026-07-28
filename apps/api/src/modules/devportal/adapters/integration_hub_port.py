"""Integration Hub port — consume-only (Phase 0+).

Developer Portal never writes Hub ORM models and never stores Hub secrets.
OAuth/credential UUIDs are pass-through references only (Architecture Lock / no peer ORM).
Usage metrics are projected via contract — Hub remains metering SoR.
"""

from datetime import date
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class DevportalIntegrationHubAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_oauth_client_ref(
        self, ctx: TenantContext, oauth_client_id: UUID | None
    ) -> UUID | None:
        """Pass-through Hub OAuth client UUID — no Hub ORM load."""
        _ = (ctx, self._db)
        return oauth_client_id

    def resolve_api_credential_ref(
        self, ctx: TenantContext, api_credential_id: UUID | None
    ) -> UUID | None:
        """Pass-through Hub API credential UUID — no Hub ORM load."""
        _ = (ctx, self._db)
        return api_credential_id

    def project_usage_metrics(
        self,
        ctx: TenantContext,
        *,
        report_type: str,
        period_start: date | None = None,
        period_end: date | None = None,
        filters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Contract projection stub — Hub remains usage metering SoR; no Hub ORM."""
        _ = (ctx, self._db)
        return {
            "source": "integration_hub",
            "report_type": report_type,
            "period_start": period_start.isoformat() if period_start else None,
            "period_end": period_end.isoformat() if period_end else None,
            "filters": filters or {},
            "metrics": {},
            "projected": True,
            "note": "Metadata projection only — Integration Hub owns metering",
        }
