import uuid


from app.services.audit_service import AuditService


class FakeAuditLogRepository:
    def __init__(self) -> None:
        self.created_logs = []

    def create(self, *, actor, action, target_type, target_id, details):
        audit_log = {
            "actor": actor,
            "action": action,
            "target_type": target_type,
            "target_id": target_id,
            "details": details,
        }
        self.created_logs.append(audit_log)
        return audit_log

    def list_all(self):
        return self.created_logs


def test_log_action_creates_audit_log() -> None:
    repository = FakeAuditLogRepository()
    service = AuditService(repository)

    target_id = uuid.uuid4()

    audit_log = service.log_action(
        actor="moustafa",
        action="CERTIFICATE_CREATED",
        target_type="CERTIFICATE",
        target_id=target_id,
        details={"common_name": "api.example.com"},
    )

    assert audit_log["actor"] == "moustafa"
    assert audit_log["action"] == "CERTIFICATE_CREATED"
    assert audit_log["target_type"] == "CERTIFICATE"
    assert audit_log["target_id"] == target_id
    assert audit_log["details"] == {"common_name": "api.example.com"}


def test_list_audit_logs_returns_logs() -> None:
    repository = FakeAuditLogRepository()
    service = AuditService(repository)

    target_id = uuid.uuid4()

    service.log_action(
        actor="moustafa",
        action="CERTIFICATE_CREATED",
        target_type="CERTIFICATE",
        target_id=target_id,
        details={"common_name": "api.example.com"},
    )

    audit_logs = service.list_audit_logs()

    assert len(audit_logs) == 1
    assert audit_logs[0]["action"] == "CERTIFICATE_CREATED"