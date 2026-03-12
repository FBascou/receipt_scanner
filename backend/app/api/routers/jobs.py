from datetime import datetime
import io
import json
from typing import Any, Dict, List
from uuid import UUID
from fastapi import Depends, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import InstrumentedAttribute, Session, selectinload
from PIL import Image
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.db.models import JobSource, JobStatus, Receipt, ReceiptJob, User
from app.schemas.receipt import PaginatedReceiptResponse, ReceiptResponse
from app.schemas.receipt_job import PaginatedJobResponse, ReceiptJobResponse
from app.services.file_service import generate_pdf_from_images
from app.services.job_service import process_receipt_job
from app.core.router import APIRouterWithErrors

# TODO:
# Add pagination to job receipts
# Add receipt image download endpoint
# Add filtering (by date / total)
# Add background processing queue
# Important: Convert job ids into YYYY_MM_DD_HH_SS_scanned_receipts

# router = APIRouter(prefix="/jobs", tags=["jobs"])
router = APIRouterWithErrors(prefix="/jobs", tags=["jobs"])

@router.post("/upload", response_model=ReceiptJobResponse)
async def upload_job(
    job_file: UploadFile,
    images: list[UploadFile],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload manually a job.json and images
    """
    return await process_receipt_job(
        db=db,
        current_user=current_user,
        job_file=job_file,
        images=images,
    )

@router.get("/", response_model=PaginatedJobResponse)
def get_jobs(
    db: Session = Depends(get_db),

    # Pagination
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),

    # Filters
    min_image_count: int | None = None,
    max_image_count: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    source: JobSource | None = None,
    status: JobStatus | None = None,

    # Sorting
    sort_by: str = Query("uploaded_at"),
    order: str = Query("desc"),
    
    # Search
    search: str | None = None,
):
    """
    Return array of jobs with filtering, pagination, sorting and search. 
    """
    
    query = db.query(ReceiptJob)

    if min_image_count is not None:
        query = query.filter(ReceiptJob.image_count >= min_image_count)

    if max_image_count is not None:
        query = query.filter(ReceiptJob.image_count <= max_image_count)

    if date_from is not None:
        query = query.filter(ReceiptJob.uploaded_at >= date_from)

    if date_to is not None:
        query = query.filter(ReceiptJob.uploaded_at <= date_to)
    
    if source is not None:
        query = query.filter(ReceiptJob.source <= source)
        
    if status is not None:
        query = query.filter(ReceiptJob.status <= status)

    if search:
        query = query.filter(ReceiptJob.raw_text.ilike(f"%{search}%"))

    # Any because columns are different types (datetime, float, str) 
    sortable_fields: Dict[str, InstrumentedAttribute[Any]] = {
        "uploaded_at": ReceiptJob.uploaded_at,
        "image_count": ReceiptJob.image_count,
    }

    if sort_by not in sortable_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    column: InstrumentedAttribute[Any] = sortable_fields[sort_by]

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    # order_by(None) removes sorting for count performance. 
    total_count = query.order_by(None).count()

    jobs = (
        query
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    
    job_responses = [
        ReceiptJobResponse.model_validate(r)
        for r in jobs
    ]

    return PaginatedJobResponse(
        total=total_count or 0,
        page=page,
        page_size=page_size,
        items=job_responses,
    )  

@router.get("/{job_id}", response_model=ReceiptJobResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    try:
        job_uuid = UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job ID")

    job = (
        db.query(ReceiptJob)
        .options(selectinload(ReceiptJob.receipts))
        .filter(ReceiptJob.id == job_uuid)
        .first()
    )

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

@router.get("/{job_id}/receipts", response_model=PaginatedReceiptResponse)
def get_job_receipts(
    job_id: UUID,
    db: Session = Depends(get_db),

    # Pagination
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),

    # Filters
    min_total: float | None = None,
    max_total: float | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,

    # Sorting
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
    
    # Search
    search: str | None = None,
):
    """
    Return array of scanned receipts data with filtering, pagination, sorting and search. 
    """
    
    query = db.query(Receipt).filter(Receipt.job_id == job_id)

    if min_total is not None:
        query = query.filter(Receipt.total >= min_total)

    if max_total is not None:
        query = query.filter(Receipt.total <= max_total)

    if date_from is not None:
        query = query.filter(Receipt.created_at >= date_from)

    if date_to is not None:
        query = query.filter(Receipt.created_at <= date_to)

    if search:
        query = query.filter(Receipt.raw_text.ilike(f"%{search}%"))

    # Any because columns are different types (datetime, float, str) 
    sortable_fields: Dict[str, InstrumentedAttribute[Any]] = {
        "created_at": Receipt.created_at,
        "total": Receipt.total,
        "date": Receipt.date,
    }

    if sort_by not in sortable_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    column: InstrumentedAttribute[Any] = sortable_fields[sort_by]

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    # order_by(None) removes sorting for count performance. 
    total_count = query.order_by(None).count()

    receipts = (
        query
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    
    receipt_responses = [
        ReceiptResponse.model_validate(r)
        for r in receipts
    ]

    return PaginatedReceiptResponse(
        total=total_count or 0,
        page=page,
        page_size=page_size,
        items=receipt_responses,
    )

@router.get("/{job_id}/download/pdf")
def download_job_pdf(job_id: str, db: Session = Depends(get_db)):
    """
    Download all receipts in a job as a single PDF.
    """
    try:
        job_uuid = UUID(job_id)  # ensures proper UUID type
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job ID")

    receipts: List[Receipt] = db.query(Receipt).filter(Receipt.job_id == job_uuid).all()

    if not receipts:
        raise HTTPException(status_code=404, detail="No receipts found for this job")

    # Convert image_data bytes into PIL Images
    images: List[Image.Image] = [
        Image.open(io.BytesIO(r.image_data)).convert("RGB") for r in receipts
    ]

    # Generate PDF from all images
    pdf_bytes = generate_pdf_from_images(images)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={job_id}.pdf"},
    )

@router.get("/{job_id}/download/json")
def download_job_json(job_id: str, db: Session = Depends(get_db)):
    """
    Download job metadata (job.json) for a batch of receipts.
    """
    try:
        job_uuid = UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job ID")

    job = db.query(ReceiptJob).filter(ReceiptJob.id == job_uuid).first()

    if not job or not job.job_json:
        raise HTTPException(status_code=404, detail="Job not found")

    return StreamingResponse(
        io.BytesIO(json.dumps(job.job_json, indent=2).encode("utf-8")),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={job_id}.json"},
    )

# @router.get("/{job_id}/download/csv")
# def download_job_csv(job_id: str, db: Session = Depends(get_db)):    