from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.enums import CertificateStatus
from app.infrastructure.database.models import CertificateModel
from app.schemas.certificate import CertificateCreate


class CertificateRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, certificate_data: CertificateCreate) -> CertificateModel:
        certificate = CertificateModel(**certificate_data.model_dump())

        self.db.add(certificate)
        self.db.commit()
        self.db.refresh(certificate)

        return certificate

    def list_all(self) -> list[CertificateModel]:
        statement = select(CertificateModel).order_by(CertificateModel.created_at.desc())
        return list(self.db.scalars(statement).all())

    def get_by_id(self, certificate_id: UUID) -> CertificateModel | None:
        return self.db.get(CertificateModel, certificate_id)

    def list_expiring(self, days: int) -> list[CertificateModel]:
        now = datetime.now(timezone.utc)
        limit_date = now + timedelta(days=days)

        statement = (
            select(CertificateModel)
            .where(CertificateModel.status == CertificateStatus.ACTIVE)
            .where(CertificateModel.not_after <= limit_date)
            .order_by(CertificateModel.not_after.asc())
        )

        return list(self.db.scalars(statement).all())

    def save(self, certificate: CertificateModel) -> CertificateModel:
        self.db.add(certificate)
        self.db.commit()
        self.db.refresh(certificate)

        return certificate