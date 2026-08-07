from typing import Optional
from sqlalchemy.orm import Session

from backend.models.user import User


def create_user(
    db: Session,
    username: str,
    email: str,
    hashed_password: str,
) -> User:

    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(
    db: Session,
    email: str,
) -> Optional[User]:

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int,
) -> Optional[User]:

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_username(
    db: Session,
    username: str,
) -> Optional[User]:

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )