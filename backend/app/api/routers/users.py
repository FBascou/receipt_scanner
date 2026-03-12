from fastapi import Depends
from app.db.models import User
from app.schemas.user import  UserResponse
from app.api.dependencies import get_current_user
from app.core.router import APIRouterWithErrors

# router = APIRouter(prefix="/users", tags=["users"])
router = APIRouterWithErrors(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user