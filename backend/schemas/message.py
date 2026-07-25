from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


# ---------------------------------------------------------
# Base Schema
# ---------------------------------------------------------

class MessageBase(BaseModel):

    role: str

    content: str


# ---------------------------------------------------------
# Create Schema
# ---------------------------------------------------------

class MessageCreate(MessageBase):

    chat_id: int


# ---------------------------------------------------------
# Update Schema
# ---------------------------------------------------------

class MessageUpdate(BaseModel):

    content: str


# ---------------------------------------------------------
# Response Schema
# ---------------------------------------------------------

class MessageResponse(MessageBase):

    id: int

    chat_id: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )