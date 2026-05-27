from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    description: str | None
    uploaded_by: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    total: int
    documents: list[DocumentResponse]