from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from app.schemas.enums import JobSource, JobStatus

class ReceiptJobCreate(BaseModel):
    source: JobSource
  
class ReceiptJobResponse(BaseModel):
    id: UUID
    uploaded_at: datetime
    source: JobSource
    image_count: int
    status: JobStatus

    class Config:
        from_attributes = True

class PaginatedJobResponse(BaseModel):
    total: int
    page: int
    page_size: int
    list: List[ReceiptJobResponse]
