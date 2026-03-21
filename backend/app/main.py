from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.core.error_handlers import validation_exception_handler
from app.db.session import engine
from app.db.base import Base
from app.api.v1.router import api_router as api_v1

# TODO: 
# How to make this async-safe (avoid blocking OCR)
# How to move processing to background tasks
# How to store images in S3 instead of DB
# How to version your job JSON (very useful later)
# How to add checksum validation
# How to support job re-processing cleanly
# Or how to reduce memory usage when streaming large PDFs
# Fix your invalid date extraction (2026-82-95)
# Improve OCR validation
# Add job progress tracking
# Optimize DB loading
# Add job progress state (PENDING → PROCESSING → PROCESSED)
# Add background task processing
# Make the upload fully asynchronous
# Add image validation (size/type limits)
# Should I use postgres? 

app = FastAPI(title="RecScan Receipt Scanner API")

# Create DB tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(api_v1, prefix="/api/v1")

# Register validation errors
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)


# UNCOMMENT FOR DEBUGGING ONLY
# from app.db.session import SessionLocal
# from app.db.models import Device, Receipt, ReceiptJob, User

# @app.get("/debug/receipts")
# def debug_receipts():
#     db = SessionLocal()
#     devices = db.query(Device).count()
#     job_count = db.query(ReceiptJob).count()
#     receipt_count = db.query(Receipt).count()
#     receipt_amount = db.query(func.sum(Receipt.total).label("receipt_amount"))

#     # return UserOverviewResponse(
#     #     devices=devices or 0,
#     #     job_count=job_count or 0,
#     #     receipt_count=receipt_count or 0,
#     #     receipt_amount= receipt_amount or 0,
#     # ) 
#     user_list = db.query(User).all()
#     db.close()
#     return {"devices": devices, "receipt_count": receipt_count, "job_count": job_count, "user_list": user_list, "receipt_amount": receipt_amount}

