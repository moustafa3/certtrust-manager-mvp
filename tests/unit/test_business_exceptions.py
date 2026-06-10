from app.services.exceptions import CertificateRevokedError


def test_business_exception_has_error_code_and_message() -> None:
    error = CertificateRevokedError()

    assert error.error_code == "CERTIFICATE_REVOKED"
    assert error.message == "A revoked certificate cannot be renewed."