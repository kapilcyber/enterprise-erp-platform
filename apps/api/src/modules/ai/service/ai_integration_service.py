"""Cross-module consume ports — Foundation audit / notification (consume only)."""

from sqlalchemy.orm import Session

from modules.ai.adapters.foundation_port import AiFoundationAdapter
from modules.foundation.service.audit_service import AuditService
from modules.foundation.service.notification_service import NotificationService


class AiIntegrationService:
    def __init__(self, db: Session) -> None:
        self.foundation = AiFoundationAdapter(db)
        self.audit = AuditService(db)
        self.notification = NotificationService(db)
