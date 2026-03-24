from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class DeviceStatus(BaseModel):
    charger: str
    battery: str
    wifi: str
    camera: str
    roller_1: str
    roller_2: str
    screen: str
    light_1: str
    light_2: str
    light_3: str
    light_4: str
    power: str
    button_1: str
    button_2: str
    button_3: str

class DeviceCreate(BaseModel):
  name: str
  mac: str
  ip: str

class DeviceResponse(BaseModel):
    id: UUID
    name: str
    mac: str
    ip: str
    # status_overview: str, status should be status: DeviceStatus
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaginatedDeviceResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[DeviceResponse]
    
    class Config:
        from_attributes = True