from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.auth import UserRegister, UserResponse, UserLogin, LoginResponse
from services.auth import register_user, login_user
from dependencies import get_current_user
from models.user import User
from schemas.auth import RefreshTokenRequest, TokenResponse
from services.auth import refresh_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=201,)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    return register_user(
        db=db,
        user_data=user_data,
    )


@router.post("/login", response_model=LoginResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return login_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
    )


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_token(
    token_data: RefreshTokenRequest,
):
    return refresh_access_token(
        token_data.refresh_token
    )
