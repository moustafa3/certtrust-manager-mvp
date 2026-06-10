from typing import Any
from uuid import UUID

from app.infrastructure.database.models import AuditLogModel
from app.infrastructure.repositories.audit_log_repository import AuditLogRepository


class AuditService:
    def __init__(self, audit_log_repository: AuditLogRepository) -> None:
        self.audit_log_repository = audit_log_repository

    def log_action(
        self,
        *,
        actor: str,
        action: str,
        target_type: str,
        target_id: UUID,
        details: dict[str, Any],
    ) -> AuditLogModel:
        return self.audit_log_repository.create(
            actor=actor,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
        )

    def list_audit_logs(self) -> list[AuditLogModel]:
        return self.audit_log_repository.list_all()