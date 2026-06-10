import logging
from datetime import datetime, timezone
from uuid import UUID

from app.domain.enums import CertificateStatus
from app.infrastructure.database.models import CertificateModel
from app.infrastructure.repositories.certificate_repository import CertificateRepository
from app.schemas.certificate import (
    CertificateCreate,
    CertificateRenewRequest,
    CertificateRevokeRequest,
)
from app.services.audit_service import AuditService
from app.services.exceptions import (
    CertificateNotFoundError,
    CertificateRevokedError,
    InvalidRenewalDateError,
    RevocationReasonRequiredError,
)

logger = logging.getLogger(__name__)


class CertificateService:
    def __init__(
        self,
        certificate_repository: CertificateRepository,
        audit_service: AuditService,
    ) -> None:
        self.certificate_repository = certificate_repository
        self.audit_service = audit_service

    def create_certificate(
        self,
        certificate_data: CertificateCreate,
        *,
        actor: str = "system",
    ) -> CertificateModel:
        certificate = self.certificate_repository.create(certificate_data)

        self.audit_service.log_action(
            actor=actor,
            action="CERTIFICATE_CREATED",
            target_type="CERTIFICATE",
            target_id=certificate.id,
            details={
                "common_name": certificate.common_name,
                "environment": certificate.environment,
            },
        )

        logger.info(
            "Certificate created | id=%s | common_name=%s | actor=%s",
            certificate.id,
            certificate.common_name,
            actor,
        )

        return certificate

    def list_certificates(self) -> list[CertificateModel]:
        return self.certificate_repository.list_all()

    def get_certificate(self, certificate_id: UUID) -> CertificateModel:
        certificate = self.certificate_repository.get_by_id(certificate_id)

        if certificate is None:
            raise CertificateNotFoundError()

        return certificate

    def list_expiring_certificates(self, days: int) -> list[CertificateModel]:
        return self.certificate_repository.list_expiring(days)

    def renew_certificate(
        self,
        certificate_id: UUID,
        request: CertificateRenewRequest,
    ) -> CertificateModel:
        certificate = self.get_certificate(certificate_id)

        if certificate.status == CertificateStatus.REVOKED:
            logger.warning(
                "Renewal refused for revoked certificate | id=%s | actor=%s",
                certificate.id,
                request.actor,
            )
            raise CertificateRevokedError()

        if request.new_not_after <= certificate.not_after:
            raise InvalidRenewalDateError()

        old_not_after = certificate.not_after
        certificate.not_after = request.new_not_after
        certificate.status = CertificateStatus.ACTIVE

        updated_certificate = self.certificate_repository.save(certificate)

        self.audit_service.log_action(
            actor=request.actor,
            action="CERTIFICATE_RENEWED",
            target_type="CERTIFICATE",
            target_id=certificate.id,
            details={
                "old_not_after": old_not_after.isoformat(),
                "new_not_after": request.new_not_after.isoformat(),
            },
        )

        logger.info(
            "Certificate renewed | id=%s | actor=%s",
            certificate.id,
            request.actor,
        )

        return updated_certificate

    def revoke_certificate(
        self,
        certificate_id: UUID,
        request: CertificateRevokeRequest,
    ) -> CertificateModel:
        certificate = self.get_certificate(certificate_id)

        if not request.reason.strip():
            raise RevocationReasonRequiredError()

        certificate.status = CertificateStatus.REVOKED
        certificate.revoked_at = datetime.now(timezone.utc)
        certificate.revocation_reason = request.reason

        updated_certificate = self.certificate_repository.save(certificate)

        self.audit_service.log_action(
            actor=request.actor,
            action="CERTIFICATE_REVOKED",
            target_type="CERTIFICATE",
            target_id=certificate.id,
            details={
                "reason": request.reason,
            },
        )

        logger.info(
            "Certificate revoked | id=%s | actor=%s | reason=%s",
            certificate.id,
            request.actor,
            request.reason,
        )

        return updated_certificate