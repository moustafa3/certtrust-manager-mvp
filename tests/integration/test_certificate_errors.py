import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_unknown_certificate_returns_404() -> None:
    unknown_id = uuid.uuid4()

    response = client.get(
        f"/api/v1/certificates/{unknown_id}",
        headers={"X-API-Key": "dev-secret-key"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "error": "CERTIFICATE_NOT_FOUND",
        "message": "Certificate not found.",
    }