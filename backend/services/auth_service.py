from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.core.security import (
    verify_password,
    hash_password,
)

from backend.core.jwt import create_access_token

from backend.crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)

from backend.schemas.user import UserCreate

def register_user(
    db: Session,
    user: UserCreate,
):

    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed = hash_password(user.password)

    return create_user(
        db=db,
        username=user.username,
        email=user.email,
        hashed_password=hashed,
    )


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):

    user = get_user_by_email(db, email)

    if user is None:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user


def login_user(
    db: Session,
    email: str,
    password: str,
):

    user = authenticate_user(
        db,
        email,
        password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
