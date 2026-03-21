from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.db.models import User, Device, ReceiptJob, Receipt
from app.schemas.user import  UserResponse, UserOverviewResponse
from app.core.router import APIRouterWithErrors

router = APIRouterWithErrors(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/overview", response_model=UserOverviewResponse)
async def get_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user),):
    """
    Return total devices, total uploaded jobs, total scanned receipts, total receipt amount
    """
    
    user_id = current_user.id

    result = db.execute(
        select(
            # devices
            select(func.count(Device.id))
            .where(Device.user_id == user_id)
            .scalar_subquery()
            .label("device_count"),

            # jobs
            select(func.count(ReceiptJob.id))
            .where(ReceiptJob.user_id == user_id)
            .scalar_subquery()
            .label("job_count"),

            # receipts
            select(func.count(Receipt.id))
            .select_from(Receipt)
            .join(ReceiptJob)
            .where(ReceiptJob.user_id == user_id)
            .scalar_subquery()
            .label("receipt_count"),

            # total amount
            select(func.coalesce(func.sum(Receipt.total), 0))
            .select_from(Receipt)
            .join(ReceiptJob)
            .where(ReceiptJob.user_id == user_id)
            .scalar_subquery()
            .label("receipt_amount"),
            
        )
    ).one()

    return UserOverviewResponse(
        devices=result.device_count,
        job_count=result.job_count,
        receipt_count=result.receipt_count,
        receipt_amount=result.receipt_amount,
    )
