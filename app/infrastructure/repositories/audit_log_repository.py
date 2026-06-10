from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.database.models import AuditLogModel


class AuditLogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        actor: str,
        action: str,
        target_type: str,
        target_id: UUID,
        details: dict[str, Any],
    ) -> AuditLogModel:
        audit_log = AuditLogModel(
            actor=actor,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
        )

        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)

        return audit_log

    def list_all(self) -> list[AuditLogModel]:
        statement = select(AuditLogModel).order_by(AuditLogModel.created_at.desc())
        return list(self.db.scalars(statement).all())