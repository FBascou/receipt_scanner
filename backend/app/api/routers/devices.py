
from typing import List, cast
from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from app.core.router import APIRouterWithErrors
from app.schemas.device import DeviceCreate, DeviceResponse, PaginatedDeviceResponse
from app.api.dependencies import get_current_user
from app.db.models import Device, User
from app.db.session import get_db

router = APIRouterWithErrors(prefix="/devices", tags=["devices"])

@router.post("/", response_model=DeviceResponse)
async def add_device(
  device_data: DeviceCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user),
):
  """
  Pair a new device with an existing user
  """
  device = Device(
      user_id=current_user.id,
      name=device_data.name,
      mac=device_data.mac,
      ip=device_data.ip,
      status="online",
  )

  db.add(device)
  db.commit()
  db.refresh(device)

  return device

@router.get("/", response_model=PaginatedDeviceResponse)
async def get_devices(
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user),
  # Pagination
  page: int = Query(1, ge=1),
  page_size: int = Query(20, ge=1, le=100),

  # Filters
  min_jobs_count: int | None = None,
  max_jobs_count: int | None = None,
  date_from: datetime | None = None,
  date_to: datetime | None = None,
  # source: JobUploadSource | None = None,
  # status: JobStatus | None = None,

  # Sorting
  sort_by: str = Query("created_at"),
  order: str = Query("desc"),
  
  # Search
  search: str | None = None,
):
  """
  Get all devices from a user
  """

  query = db.query(Device).filter(Device.user_id == current_user.id)
  
  total_count = query.order_by(None).count()
  
  devices = (
      query
      .offset((page - 1) * page_size)
      .limit(page_size)
      .all()
  )
    
  
  # device_responses = [
  #     DeviceResponse.model_validate(d)
  #     for d in devices
  # ]

  return PaginatedDeviceResponse(
    total=total_count or 0,
    page=page,
    page_size=page_size,
    items=cast(List[DeviceResponse], devices),
  )  
  
@router.get("/{id}", response_model=DeviceResponse)
async def get_device(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    device = db.query(Device).filter(
        Device.id == id,
        Device.user_id == current_user.id
    ).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device

@router.delete("/{id}", response_model=DeviceResponse)
async def delete_device(device_data: DeviceCreate):
  return

@router.patch("/{id}", response_model=DeviceResponse)
async def patch_device(device_data: DeviceCreate):
  return

@router.post("/status", response_model=DeviceResponse)
async def send_device_status(device_data: DeviceCreate):
  return

@router.get("/status", response_model=DeviceResponse)
async def get_device_status(device_data: DeviceCreate):
  return