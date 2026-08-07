from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import verify_access_token
from backend.crud.user import get_user_by_id

from backend.core.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    print("=" * 60)
    print("TOKEN:", token)

    payload = verify_access_token(token)
    print("PAYLOAD:", payload)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user_id = payload.get("sub")
    print("USER_ID:", user_id)

    user = get_user_by_id(db, int(user_id))
    print("USER:", user)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user