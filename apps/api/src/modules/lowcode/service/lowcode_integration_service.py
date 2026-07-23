"""Cross-module consume ports — Phase 1 stubs (no peer ORM writes)."""

from sqlalchemy.orm import Session

from modules.lowcode.adapters.foundation_port import LowcodeFoundationAdapter


class LowcodeIntegrationService:
    def __init__(self, db: Session) -> None:
        self.foundation = LowcodeFoundationAdapter(db)
