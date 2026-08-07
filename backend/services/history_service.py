from pathlib import Path
from datetime import datetime
import uuid
from typing import Optional

from backend.services.chat_service import chat_model
from backend.models.chat import Chat
from backend.models.message import Message

from sqlalchemy.orm import Session

from backend.crud.chat import create_chat as crud_create_chat

from backend.crud.chat import (
    get_chat,
    get_all_chats,
    rename_chat,
    delete_chat,
    touch_chat,
    chat_exists,
    chat_count,
)

from backend.crud.message import (
    create_message,
    get_chat_messages,
    delete_chat_messages,
)

# -------------------------------------------------
# Project Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHAT_DIR = PROJECT_ROOT / "chats"

CHAT_DIR.mkdir(exist_ok=True)


# -------------------------------------------------
# Timestamp
# -------------------------------------------------

def current_time() -> str:
    """
    Returns current timestamp in ISO format.
    """

    return datetime.now().isoformat()


# -------------------------------------------------
# Chat File Path
# -------------------------------------------------

def chat_path(chat_id: str) -> Path:
    """
    Returns the JSON path of a chat.
    """

    return CHAT_DIR / f"{chat_id}.json"


# -------------------------------------------------
# Create New Chat
# -------------------------------------------------

def create_chat(
    db: Session,
    user_id: int,
    title: str = "New Chat",
):
    return crud_create_chat(
        db=db,
        user_id=user_id,
        title=title,
    )


def load_chat(
    db: Session,
    chat_id: int,
    user_id: int,
) -> Optional[Chat]:

    return get_chat(
        db=db,
        chat_id=chat_id,
        user_id=user_id
    )

# -------------------------------------------------
# List Chats
# -------------------------------------------------

def list_chats(
    db: Session,
    user_id: int,
):
    """
    Returns all chats for the current user,
    sorted by latest update.
    """

    return get_all_chats(
        db=db,
        user_id=user_id,
    )


def generate_ai_title(first_message: str):

    prompt = f"""
Generate a concise conversation title.

Rules:
- Maximum 6 words
- No quotation marks
- No punctuation at the end

Conversation:
{first_message}
"""

    return chat_model.invoke(prompt).content.strip()     


def update_chat_title(
    db: Session,
    chat_id: int,
    new_title: str,
):

    return rename_chat(
        db=db,
        chat_id=chat_id,
        new_title=new_title,
    )


def remove_chat(
    db: Session,
    chat_id: int,
):

    return delete_chat(
        db=db,
        chat_id=chat_id,
    )

def save_user_message(
    db: Session,
    chat_id: int,
    content: str,
) -> Message:

    return create_message(
        db=db,
        chat_id=chat_id,
        role="user",
        content=content,
    )

def save_ai_message(
    db: Session,
    chat_id: int,
    content: str,
) -> Message:

    return create_message(
        db=db,
        chat_id=chat_id,
        role="assistant",
        content=content,
    )

def load_chat_history(
    db: Session,
    chat_id: int,
):

    return get_chat_messages(
        db=db,
        chat_id=chat_id,
    )


def clear_chat_history(
    db: Session,
    chat_id: int,
):

    return delete_chat_messages(
        db=db,
        chat_id=chat_id,
    )

def update_timestamp(
    db: Session,
    chat_id: int,
):

    touch_chat(
        db=db,
        chat_id=chat_id,
    )


def exists(
    db: Session,
    chat_id: int,
):

    return chat_exists(
        db=db,
        chat_id=chat_id,
    )


def total_chats(
    db: Session,
):

    return chat_count(db)



def save_chat(
    db: Session,
    chat_id: int,
    role: str,
    content: str,
):
    """
    Save a single message to an existing chat.

    Args:
        db: SQLAlchemy session
        chat_id: Chat ID
        role: "user", "assistant", or "system"
        content: Message text
    """

    chat = get_chat(db, chat_id)

    if chat is None:
        raise ValueError(f"Chat {chat_id} does not exist.")

    return create_message(
        db=db,
        chat_id=chat_id,
        role=role,
        content=content,
    )