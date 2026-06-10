class BusinessError(Exception):
    error_code = "BUSINESS_ERROR"
    message = "A business error occurred."


class CertificateNotFoundError(BusinessError):
    error_code = "CERTIFICATE_NOT_FOUND"
    message = "Certificate not found."


class CertificateRevokedError(BusinessError):
    error_code = "CERTIFICATE_REVOKED"
    message = "A revoked certificate cannot be renewed."


class RevocationReasonRequiredError(BusinessError):
    error_code = "REVOCATION_REASON_REQUIRED"
    message = "A revocation reason is required."


class InvalidRenewalDateError(BusinessError):
    error_code = "INVALID_RENEWAL_DATE"
    message = "The new expiration date must be after the current expiration date."