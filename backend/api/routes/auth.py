from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db

from backend.schemas.user import (
    UserLogin,
    Token,
    UserCreate,
    UserResponse,
    UserBase
)

from backend.services.auth_service import (
    login_user,
    register_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    request: UserLogin,
    db: Session = Depends(get_db),
):

    return login_user(
        db=db,
        email=request.email,
        password=request.password,
    )

@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    request: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(
        db=db,
        user=request,
    )

