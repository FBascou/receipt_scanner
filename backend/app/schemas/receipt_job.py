from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from app.schemas.enums import JobUploadSource, JobStatus

class ReceiptJobCreate(BaseModel):
    source: JobUploadSource
  
class ReceiptJobResponse(BaseModel):
    id: UUID
    # device_id
    # total_amount
    uploaded_at: datetime
    source: JobUploadSource
    image_count: int
    status: JobStatus

    class Config:
        from_attributes = True

class PaginatedJobResponse(BaseModel):
    # total_pages
    total: int
    page: int
    page_size: int
    items: List[ReceiptJobResponse]
