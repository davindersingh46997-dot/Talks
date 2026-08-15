from typing import Optional

from sqlalchemy.orm import Session

from backend.models.chat import Chat


# ---------------------------------------------------------
# Create Chat
# ---------------------------------------------------------

def create_chat(
    db: Session,
    user_id: int,
    title: str = "New Chat",
) -> Chat:

    chat = Chat(
        title=title,
        user_id=user_id,
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


# ---------------------------------------------------------
# Get Chat by ID
# ---------------------------------------------------------

def get_chat(
    db: Session,
    chat_id: int,
    user_id: int,
) -> Optional[Chat]:

    return (
        db.query(Chat)
        .filter(
            Chat.id == chat_id,
            Chat.user_id == user_id,
        )
        .first()
    )


# ---------------------------------------------------------
# Get All Chats
# ---------------------------------------------------------

def get_all_chats(
    db: Session,
    user_id: int,
):

    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id)
        .order_by(Chat.updated_at.desc())
        .all()
    )


# ---------------------------------------------------------
# Rename Chat
# ---------------------------------------------------------

def rename_chat(
    db: Session,
    chat_id: int,
    user_id: int,
    new_title: str,
) -> Optional[Chat]:

    chat = get_chat(
        db=db,
        chat_id=chat_id,
        user_id=user_id,
    )

    if chat is None:
        return None

    chat.title = new_title

    db.commit()
    db.refresh(chat)

    return chat


# ---------------------------------------------------------
# Delete Chat
# ---------------------------------------------------------

def delete_chat(
    db: Session,
    chat_id: int,
    user_id: int,
) -> bool:

    chat = get_chat(
        db=db,
        chat_id=chat_id,
        user_id=user_id,
    )

    if chat is None:
        return False

    db.delete(chat)
    db.commit()

    return True


# ---------------------------------------------------------
# Update Timestamp
# ---------------------------------------------------------

def touch_chat(
    db: Session,
    chat_id: int,
    user_id: int,
):

    chat = get_chat(
        db=db,
        chat_id=chat_id,
        user_id=user_id,
    )

    if chat is None:
        return

    db.add(chat)
    db.commit()


# ---------------------------------------------------------
# Chat Exists
# ---------------------------------------------------------

def chat_exists(
    db: Session,
    chat_id: int,
    user_id: int,
) -> bool:

    return (
        db.query(Chat)
        .filter(
            Chat.id == chat_id,
            Chat.user_id == user_id,
        )
        .first()
        is not None
    )


# ---------------------------------------------------------
# Chat Count
# ---------------------------------------------------------

def chat_count(
    db: Session,
    user_id: int,
) -> int:

    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id)
        .count()
    )