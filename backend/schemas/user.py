from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import ConfigDict


class UserBase(BaseModel):

    username: str
    email: EmailStr


class UserCreate(UserBase):

    password: str


class UserLogin(BaseModel):

    email: EmailStr
    password: str


class Token(BaseModel):

    access_token: str
    token_type: str


class UserResponse(UserBase):

    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )