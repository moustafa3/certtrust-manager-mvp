from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.dependencies import ApiKeyAuth
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.audit_log_repository import AuditLogRepository
from app.schemas.audit_log import AuditLogRead
from app.services.audit_service import AuditService

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


def get_audit_service(
    db: Annotated[Session, Depends(get_db)],
) -> AuditService:
    audit_log_repository = AuditLogRepository(db)
    return AuditService(audit_log_repository)


@router.get("", response_model=list[AuditLogRead])
def list_audit_logs(
    service: Annotated[AuditService, Depends(get_audit_service)],
    _: ApiKeyAuth,
) -> list[AuditLogRead]:
    audit_logs = service.list_audit_logs()
    return [AuditLogRead.model_validate(audit_log) for audit_log in audit_logs]