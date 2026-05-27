from pydantic import BaseModel
from datetime import datetime


class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    question: str
    answer: str
    sources: list | None
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogListResponse(BaseModel):
    total: int
    logs: list[AuditLogResponse]