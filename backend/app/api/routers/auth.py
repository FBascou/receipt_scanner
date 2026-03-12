from fastapi import  Depends
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import EmailAlreadyRegistered, InvalidCredentials, UserNotFound
from app.db.session import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.auth import Token
from app.core.router import APIRouterWithErrors

router = APIRouterWithErrors(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise UserNotFound()

    if not verify_password(data.password, user.hashed_password):
        raise InvalidCredentials()

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == user.email).first():
        raise EmailAlreadyRegistered()

    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user