import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import CertificateEnvironment, CertificateStatus
from app.infrastructure.database.session import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CertificateModel(Base):
    __tablename__ = "certificates"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    common_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    issuer: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[CertificateStatus] = mapped_column(
        Enum(CertificateStatus, name="certificate_status"),
        nullable=False,
        default=CertificateStatus.ACTIVE,
    )
    environment: Mapped[CertificateEnvironment] = mapped_column(
        Enum(CertificateEnvironment, name="certificate_environment"),
        nullable=False,
    )
    owner_team: Mapped[str] = mapped_column(String(120), nullable=False)
    not_before: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    not_after: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    revocation_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)


class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    actor: Mapped[str] = mapped_column(String(120), nullable=False)
    action: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(120), nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )