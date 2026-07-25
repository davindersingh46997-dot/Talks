from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

from backend.schemas.message import MessageResponse


# ---------------------------------------------------------
# Base Schema
# ---------------------------------------------------------

class ChatBase(BaseModel):

    title: str


# ---------------------------------------------------------
# Create Schema
# ---------------------------------------------------------

class ChatCreate(ChatBase):

    user_id: int | None = None


# ---------------------------------------------------------
# Rename Schema
# ---------------------------------------------------------

class ChatRename(BaseModel):

    title: str


# ---------------------------------------------------------
# Chat List Item
# ---------------------------------------------------------

class ChatSummary(BaseModel):

    id: int

    title: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------------------------------------------------
# Complete Chat
# ---------------------------------------------------------

class ChatResponse(ChatSummary):

    messages: list[MessageResponse] = []