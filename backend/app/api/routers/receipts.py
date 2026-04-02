from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import UUID, uuid4
from fastapi import  Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.db.models import JobUploadSource, JobStatus, Receipt, ReceiptJob, User
from app.services.ocr_service import process_image
from app.services.parser import sanitize_ocr_date
from app.schemas.receipt import ReceiptResponse
from app.schemas.receipt_job import ReceiptJobResponse
from app.core.router import APIRouterWithErrors
from app.core.exceptions import DeviceRequired

# TODO:
# Add pagination to job receipts
# Add receipt image download endpoint
# Add filtering (by date / total)
# Add background processing queue

router = APIRouterWithErrors(prefix="/scan", tags=["scan"])

@router.post("/single", response_model=ReceiptResponse)
async def scan_receipt(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    device_id: UUID | None = None
):
    """
    Scan single receipt image.
    Generates:
      - Receipts in DB
      - Job metadata JSON
      - Optional image URLs
    """
    
    if device_id is None:
        # manual upload
        source = JobUploadSource.MANUAL
    else:
        source = JobUploadSource.AUTOMATIC
    #  source = ( JobUploadSource.AUTOMATIC if device_id else JobUploadSource.MANUAL)
    
    idDevice =  device_id if device_id else "N/A"
    
    # This should go in APIRouterWithErrors
    if source == JobUploadSource.AUTOMATIC and not device_id:
        raise DeviceRequired()
    
    # Read uploaded file
    image_bytes = await file.read()

    # Run OCR
    receipt_data = process_image(image_bytes)

    # Find or create a pending job
    job = (
        db.query(ReceiptJob)
        .filter(ReceiptJob.user_id == current_user.id, ReceiptJob.status == JobStatus.PENDING)
        .first()
    )

    if not job:
        job = ReceiptJob(
            id=uuid4(),
            user_id=current_user.id,
            # device_id=device_id,
            device_id=idDevice,
            status=JobStatus.PENDING,
            source=source,
            uploaded_at=datetime.now(timezone.utc),
            image_count=1,  # First image
        )
        db.add(job)
        db.commit()
        db.refresh(job)
    else:
        # Increment image count safely
        job.image_count = (job.image_count or 0) + 1
        db.commit()
        db.refresh(job)

    # Generate a unique image URL (optional, e.g., for static file serving)
    image_url = f"/receipts/{uuid4()}.jpeg"

    # Create the receipt
    db_receipt = Receipt(
        id=uuid4(),
        job_id=job.id,
        total=receipt_data.total or 0.0,
        date=sanitize_ocr_date(receipt_data.date),
        raw_text=receipt_data.raw_text or "",
        image_data=image_bytes,
        image_url=image_url,
        created_at=datetime.now(timezone.utc),
    )

    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)

    return db_receipt

@router.post("/batch", response_model=ReceiptJobResponse)
async def scan_receipts(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    device_id: UUID | None = None
):
    """
    Scan multiple receipt images in one job.
    Generates:
      - Receipts in DB
      - Job metadata JSON
      - Optional image URLs
    """

    source = (JobUploadSource.AUTOMATIC if device_id else JobUploadSource.MANUAL)
    
    # This should go in APIRouterWithErrors
    if source == JobUploadSource.AUTOMATIC and not device_id:
        raise DeviceRequired()

    # Create a new ReceiptJob for this batch
    job = ReceiptJob(
        id=uuid4(),
        user_id=current_user.id,
        device_id=device_id,
        status=JobStatus.PENDING,
        source=source,
        uploaded_at=datetime.now(timezone.utc),
        image_count=len(files),
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    receipts: List[Receipt] = []

    for file in files:
        image_bytes = await file.read()
        receipt_data = process_image(image_bytes)

        db_receipt = Receipt(
            id=uuid4(),
            job_id=job.id,
            total=receipt_data.total or 0.0,
            date=receipt_data.date or "unknown",
            raw_text=receipt_data.raw_text or "",
            image_data=image_bytes,
            image_url=f"/receipts/{uuid4()}.jpeg",  # optional
            created_at=datetime.now(timezone.utc),
        )
        db.add(db_receipt)
        receipts.append(db_receipt)

    db.commit()

    # Attach receipts to job for response
    job.receipts = receipts

    # Generate job.json metadata
    job_json: Dict[str, Any] = {
        "id": str(job.id),
        "user_id": str(current_user.id),
        "uploaded_at": job.uploaded_at.isoformat(),
        "source": job.source.value,
        "image_count": job.image_count,
        "status": job.status.value,
        "receipts": [
            {
                "id": str(r.id),
                "date": r.date,
                "total": r.total,
                "raw_text": r.raw_text,
                "created_at": r.created_at.isoformat(),
            }
            for r in receipts
        ],
    }
    
    job.job_json = job_json   
    db.commit()

    return job