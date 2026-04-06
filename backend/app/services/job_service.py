from datetime import datetime, timezone
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.db.models import Device, JobStatus, ReceiptJob, Receipt, User
from app.schemas.receipt_job import ReceiptJobCreate
from app.services.ocr_service import process_image
from app.core.exceptions import DeviceInvalid

# This is your orchestration + persistence layer - Used by API endpoint
# ReceiptJob DB model is created
# Receipt DB models are created
# Foreign keys assigned
# Everything committed    
# Check for dates

async def process_receipt_job(
    db: Session,
    current_user: User,
    job_file: UploadFile,
    images: list[UploadFile],
) -> ReceiptJob:

    job_data = await job_file.read()
    job_schema = ReceiptJobCreate.model_validate_json(job_data)
    device_id = job_schema.device_id
    
    if device_id:
        device = db.query(Device).filter(
        Device.id == device_id,
        Device.user_id == current_user.id
    ).first()

        if not device:
            raise DeviceInvalid()

    db_job = ReceiptJob(
        id=uuid4(),
        user_id=current_user.id,
        device_id=device_id,
        total_amount=0.0,  
        source=job_schema.source,
        image_count=len(images),
        status=JobStatus.PENDING,
        job_json=job_schema.model_dump(),
    )

    db.add(db_job)
    db.flush()

    total_amount = 0.0 

    for image in images:
        image_bytes = await image.read()
        receipt_schema = process_image(image_bytes)

        total_amount += receipt_schema.total_amount

        db_receipt = Receipt(
            id=uuid4(),
            job_id=db_job.id,
            image_data=image_bytes,
            total_amount=receipt_schema.total_amount, 
            date=receipt_schema.date,
            raw_text=receipt_schema.raw_text,
            created_at=datetime.now(timezone.utc),
        )

        db.add(db_receipt)

    db_job.total_amount = total_amount 
    db_job.status = JobStatus.PROCESSED

    db.commit()
    db.refresh(db_job)

    return db_job