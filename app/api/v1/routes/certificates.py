from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.dependencies import ApiKeyAuth
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.audit_log_repository import AuditLogRepository
from app.infrastructure.repositories.certificate_repository import CertificateRepository
from app.schemas.certificate import (
    CertificateCreate,
    CertificateRead,
    CertificateRenewRequest,
    CertificateRevokeRequest,
)
from app.services.audit_service import AuditService
from app.services.certificate_service import CertificateService

router = APIRouter(
    prefix="/certificates",
    tags=["Certificates"],
)


def get_certificate_service(
    db: Annotated[Session, Depends(get_db)],
) -> CertificateService:
    certificate_repository = CertificateRepository(db)
    audit_log_repository = AuditLogRepository(db)
    audit_service = AuditService(audit_log_repository)

    return CertificateService(
        certificate_repository=certificate_repository,
        audit_service=audit_service,
    )


@router.post("", response_model=CertificateRead, status_code=201)
def create_certificate(
    certificate_data: CertificateCreate,
    service: Annotated[CertificateService, Depends(get_certificate_service)],
    _: ApiKeyAuth,
) -> CertificateRead:
    certificate = service.create_certificate(certificate_data)
    return CertificateRead.model_validate(certificate)


@router.get("", response_model=list[CertificateRead])
def list_certificates(
    service: Annotated[CertificateService, Depends(get_certificate_service)],
    _: ApiKeyAuth,
) -> list[CertificateRead]:
    certificates = service.list_certificates()
    return [CertificateRead.model_validate(certificate) for certificate in certificates]


@router.get("/expiring", response_model=list[CertificateRead])
def list_expiring_certificates(
    service: Annotated[CertificateService, Depends(get_certificate_service)],
    _: ApiKeyAuth,
    days: int = Query(default=30, ge=1, le=365),
) -> list[CertificateRead]:
    certificates = service.list_expiring_certificates(days)
    return [CertificateRead.model_validate(certificate) for certificate in certificates]


@router.get("/{certificate_id}", response_model=CertificateRead)
def get_certificate(
    certificate_id: UUID,
    service: Annotated[CertificateService, Depends(get_certificate_service)],
    _: ApiKeyAuth,
) -> CertificateRead:
    certificate = service.get_certificate(certificate_id)
    return CertificateRead.model_validate(certificate)


@router.post("/{certificate_id}/renew", response_model=CertificateRead)
def renew_certificate(
    certificate_id: UUID,
    request: CertificateRenewRequest,
    service: Annotated[CertificateService, Depends(get_certificate_service)],
    _: ApiKeyAuth,
) -> CertificateRead:
    certificate = service.renew_certificate(certificate_id, request)
    return CertificateRead.model_validate(certificate)


@router.post("/{certificate_id}/revoke", response_model=CertificateRead)
def revoke_certificate(
    certificate_id: UUID,
    request: CertificateRevokeRequest,
    service: Annotated[CertificateService, Depends(get_certificate_service)],
    _: ApiKeyAuth,
) -> CertificateRead:
    certificate = service.revoke_certificate(certificate_id, request)
    return CertificateRead.model_validate(certificate)