from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from app.schemas.receipt_job import PaginatedJobResponse

class DeviceCreate(BaseModel):
  user_id: UUID
  name: str
  mac: str
  ip: str

class DeviceResponse(BaseModel):
    id: UUID
    name: str
    mac: str
    ip: str
    # create enum for status
    status: str
    job_list: Optional[PaginatedJobResponse] = None
    created_at: datetime

class PaginatedDeviceResponse(BaseModel):
    total: int
    page: int
    page_size: int
    list: List[DeviceResponse]