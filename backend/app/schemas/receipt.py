import re
from typing import List
from pydantic import BaseModel, field_validator
from datetime import datetime
from uuid import UUID

class ReceiptCreate(BaseModel):
    date: str
    total: float
    raw_text: str

    @field_validator("total")
    @classmethod
    def validate_total(cls, v: float):
        if v < 0:
            raise ValueError("total must be >= 0")
        return v

    @field_validator("date")
    @classmethod
    def normalize_date(cls, v: str):
        if v.lower() == "unknown":
            return "unknown"

        match = re.match(r"(\d{2})[.\-](\d{2})[.\-](\d{4})", v)
        if match:
            day, month, year = match.groups()
            return f"{year}-{month}-{day}"

        return v

class ReceiptResponse(BaseModel):
    id: UUID
    date: str
    total: float
    raw_text: str
    created_at: datetime

    class Config:
        from_attributes = True  # important for SQLAlchemy

class PaginatedReceiptResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ReceiptResponse]
    
    class Config:
        from_attributes = True
