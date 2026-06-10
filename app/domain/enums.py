from enum import StrEnum


class CertificateStatus(StrEnum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    PENDING_RENEWAL = "PENDING_RENEWAL"


class CertificateEnvironment(StrEnum):
    DEV = "DEV"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"