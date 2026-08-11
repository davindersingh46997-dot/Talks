from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import verify_access_token
from backend.crud.user import get_user_by_id

from backend.core.database import SessionLocal

from jose import jwt, JWTError
from backend.models.user import User

from backend.core.config import settings


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
    print("TOKEN:", token)

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )

        print("DECODED PAYLOAD:", payload)

        user_id = payload.get("sub")

        print("USER ID FROM TOKEN:", user_id)

        if user_id is None:
            print("❌ No user_id in token")

            raise HTTPException(
                status_code=401,
                detail="Invalid token: no user ID",
            )

        user = db.query(User).filter(
            User.id == int(user_id)
        ).first()

        print("USER FROM DATABASE:", user)

        if user is None:
            print("❌ User does not exist")

            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        print("✅ AUTHENTICATED USER:", user.id)

        return user

    except JWTError as e:
        print("❌ JWT ERROR:", repr(e))

        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    except Exception as e:
        print("❌ AUTH ERROR:", repr(e))

        raise HTTPException(
            status_code=401,
            detail="Authentication failed",
        )