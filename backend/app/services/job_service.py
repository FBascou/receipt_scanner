from datetime import datetime, timezone
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.db.models import JobStatus, ReceiptJob, Receipt, User
from app.schemas.receipt_job import ReceiptJobCreate
from app.services.ocr_service import process_image

# This is your orchestration + persistence layer - Used by API endpoint
# ReceiptJob DB model is created
# Receipt DB models are created
# Foreign keys assigned
# Everything committed    
# Check for dates

# async def process_receipt_job(
#     db: Session,
#     current_user: User,
#     job_file: UploadFile,
#     images: list[UploadFile],
# ) -> ReceiptJob:

#     # Parse job.json
#     job_data = await job_file.read()
#     job_schema = ReceiptJobCreate.model_validate_json(job_data)

#     if job_schema.image_count != len(images):
#         raise ValueError("Image count mismatch")

#     # Create DB Job
#     db_job = ReceiptJob(
#         user_id=current_user.id,
#         source=job_schema.source,
#         image_count=len(images),
#         status=JobStatus.PENDING,
#     )

#     db.add(db_job)
#     db.flush()

#     # Process each image
#     for image in images:
#         image_bytes = await image.read()

#         # OCR should accept bytes now (modify process_image)
#         receipt_schema = process_image(image_bytes)

#         db_receipt = Receipt(
#             job_id=db_job.id,
#             user_id=current_user.id,
#             image_data=image_bytes,
#             **receipt_schema.model_dump(),
#         )

#         db.add(db_receipt)

#     db_job.status = JobStatus.PROCESSED

#     db.commit()
#     db.refresh(db_job)

#     return db_job

async def process_receipt_job(
    db: Session,
    current_user: User,
    job_file: UploadFile,
    images: list[UploadFile],
) -> ReceiptJob:

    job_data = await job_file.read()
    job_schema = ReceiptJobCreate.model_validate_json(job_data)

    db_job = ReceiptJob(
        id=uuid4(),
        user_id=current_user.id,
        source=job_schema.source,
        image_count=len(images), 
        status=JobStatus.PENDING,
        job_json=job_schema.model_dump(),
    )

    db.add(db_job)
    db.flush()

    for image in images:
        image_bytes = await image.read()
        receipt_schema = process_image(image_bytes)

        db_receipt = Receipt(
            id=uuid4(),
            job_id=db_job.id,
            image_data=image_bytes,
            total=receipt_schema.total,
            date=receipt_schema.date,
            raw_text=receipt_schema.raw_text,
            created_at=datetime.now(timezone.utc),
        )

        db.add(db_receipt)

    db_job.status = JobStatus.PROCESSED

    db.commit()
    db.refresh(db_job)

    return db_job