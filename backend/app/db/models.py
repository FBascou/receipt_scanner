from datetime import datetime, timezone
from typing import Any
from sqlalchemy import JSON, Enum, Index, LargeBinary, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import uuid4, UUID as UUIDType
from app.db.base import Base
from enum import Enum as PyEnum

class JobStatus(str, PyEnum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

class JobUploadSource(str, PyEnum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    devices = relationship(
        "Device",
        back_populates="user",
        cascade="all, delete"
    )

    jobs = relationship(
        "ReceiptJob",
        back_populates="user",
        cascade="all, delete"
    )

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUIDType] = mapped_column( UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    name: Mapped[str] = mapped_column(String)
    mac: Mapped[str] = mapped_column(String)
    ip: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="devices")
    jobs = relationship("ReceiptJob", back_populates="device")

    __table_args__ = (
        Index("idx_device_user_id", "user_id"),
    )

class ReceiptJob(Base):
    __tablename__ = "receipt_jobs"

    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    device_id: Mapped[UUIDType | None] = mapped_column( UUID(as_uuid=True), ForeignKey("devices.id"), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    source: Mapped[JobUploadSource] = mapped_column(Enum(JobUploadSource), default=JobUploadSource.AUTOMATIC)
    image_count: Mapped[int] = mapped_column(Integer)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.PENDING)
    job_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    
    user = relationship("User", back_populates="jobs")
    device = relationship("Device", back_populates="jobs")
    receipts = relationship("Receipt", back_populates="job")
    
    __table_args__ = (
        Index("idx_job_user_id", "user_id"),
    )
    
class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True) ,primary_key=True, default=uuid4)
    job_id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), ForeignKey("receipt_jobs.id"))
    date: Mapped[str] = mapped_column(String)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    image_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    raw_text: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    job = relationship("ReceiptJob", back_populates="receipts")
    
    __table_args__ = (
        Index("idx_receipt_job_id", "job_id"),
        Index("idx_receipt_created_at", "created_at"),
        Index("idx_receipt_total", "total"),
    )
