"""Business module port — contract key pass-through for tool contract_key (NO peer ORM)."""

from sqlalchemy.orm import Session

from modules.foundation.domain.value_objects import TenantContext


class AiBusinessModuleAdapter:
    def __init__(self, db: Session) -> None:
        self._db = db

    def resolve_contract_key(
        self, ctx: TenantContext, contract_key: str | None
    ) -> str | None:
        """Pass-through module service contract key — no peer ORM load."""
        _ = (ctx, self._db)
        return contract_key
