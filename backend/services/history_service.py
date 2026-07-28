from pathlib import Path
from datetime import datetime
import uuid

from services.chat_service import chat_model

from sqlalchemy.orm import Session
from models.chat import Chat

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
    title: str = "New Chat"
):
    """
    Creates a new chat in the database.

    Returns:
        chat_id
    """

    chat = Chat(
        title=title,
        user_id=user_id
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat.id


def load_chat(
    db : Session,
    
)


def save_chat(chat: dict):
    """
    Saves a chat dict to JSON file.
    """

    chat["updated_at"] = current_time()

    path = chat_path(chat["id"])

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            chat,
            file,
            indent=4,
            ensure_ascii=False
        )

# -------------------------------------------------
# List Chats
# -------------------------------------------------

def list_chats():
    """
    Returns all chats sorted by latest update.
    """

    chats = []

    for file in CHAT_DIR.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:

            chats.append(
                json.load(f)
            )

    chats.sort(
        key=lambda x: x["updated_at"],
        reverse=True
    )

    return chats  


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