from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
from datetime import datetime
from app.api.utils import validate_password_strength

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator("password")
    def validate_password_field(cls, v: str):
        return validate_password_strength(v)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator("password")
    def validate_password_field(cls, v: str):
        return validate_password_strength(v)

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
        
class UserPasswordChange(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    def validate_new_password(cls, v: str):
        return validate_password_strength(v)
    
class UserOverviewResponse(BaseModel): 
    devices: int
    job_count: int
    receipt_count: int
    receipt_amount: float