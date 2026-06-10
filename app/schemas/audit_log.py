from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditLogRead(BaseModel):
    id: UUID
    actor: str
    action: str
    target_type: str
    target_id: UUID
    details: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)