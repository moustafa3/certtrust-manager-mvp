from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.enums import CertificateEnvironment, CertificateStatus


class CertificateCreate(BaseModel):
    common_name: str = Field(min_length=3, max_length=255)
    issuer: str = Field(min_length=2, max_length=255)
    environment: CertificateEnvironment
    owner_team: str = Field(min_length=2, max_length=120)
    not_before: datetime
    not_after: datetime

    @field_validator("not_after")
    @classmethod
    def validate_not_after(cls, not_after: datetime, info) -> datetime:
        not_before = info.data.get("not_before")

        if not_before and not_after <= not_before:
            raise ValueError("not_after must be greater than not_before")

        return not_after


class CertificateRead(BaseModel):
    id: UUID
    common_name: str
    issuer: str
    status: CertificateStatus
    environment: CertificateEnvironment
    owner_team: str
    not_before: datetime
    not_after: datetime
    created_at: datetime
    updated_at: datetime
    revoked_at: datetime | None
    revocation_reason: str | None

    model_config = ConfigDict(from_attributes=True)


class CertificateRenewRequest(BaseModel):
    actor: str = Field(min_length=2, max_length=120)
    new_not_after: datetime


class CertificateRevokeRequest(BaseModel):
    actor: str = Field(min_length=2, max_length=120)
    reason: str = Field(min_length=3, max_length=500)


class CertificateExpiringQuery(BaseModel):
    days: int = Field(default=30, ge=1, le=365)