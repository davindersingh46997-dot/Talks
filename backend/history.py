import json
import uuid

from pathlib import Path
from datetime import datetime

from backend.bot import chat_model


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

def create_chat(title: str = "New Chat") -> str:
    """
    Creates a new chat JSON file.

    Returns:
        chat_id
    """

    chat_id = f"chat_{uuid.uuid4().hex[:8]}"

    now = current_time()

    chat = {
        "id": chat_id,
        "title": title,
        "created_at": now,
        "updated_at": now,
        "messages": []
    }

    path = chat_path(chat_id)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            chat,
            file,
            indent=4,
            ensure_ascii=False
        )

    return chat_id


def load_chat(chat_id: str) -> dict:
    """
    Loads a chat JSON file.

    Returns:
        chat dict
    """

    path = chat_path(chat_id)

    with open(path, "r", encoding="utf-8") as file:
        chat = json.load(file)     

    return chat


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