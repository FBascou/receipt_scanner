from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from app.schemas.enums import JobUploadSource, JobStatus

class ReceiptJobCreate(BaseModel):
    device_id: UUID | None = None
    source: JobUploadSource
  
class ReceiptJobResponse(BaseModel):
    id: UUID
    device_id: UUID | None 
    total_amount: float
    uploaded_at: datetime
    image_count: int
    source: JobUploadSource
    status: JobStatus

    class Config:
        from_attributes = True

class PaginatedJobResponse(BaseModel):
    total_pages: int
    page: int
    page_size: int
    items: List[ReceiptJobResponse]
