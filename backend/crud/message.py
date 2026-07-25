from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from backend.models.message import Message
from backend.models.chat import Chat


# ---------------------------------------------------------
# Create Message
# ---------------------------------------------------------

def create_message(
    db: Session,
    chat_id: int,
    role: str,
    content: str,
) -> Message:

    message = Message(
        chat_id=chat_id,
        role=role,
        content=content,
    )

    db.add(message)

    # Update chat timestamp
    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id)
        .first()
    )

    if chat:
        db.add(chat)

    db.commit()
    db.refresh(message)

    return message


# ---------------------------------------------------------
# Get Message
# ---------------------------------------------------------

def get_message(
    db: Session,
    message_id: int,
) -> Optional[Message]:

    return (
        db.query(Message)
        .filter(Message.id == message_id)
        .first()
    )


# ---------------------------------------------------------
# Get Messages of a Chat
# ---------------------------------------------------------

def get_chat_messages(
    db: Session,
    chat_id: int,
) -> List[Message]:

    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
        .all()
    )


# ---------------------------------------------------------
# Get Last Message
# ---------------------------------------------------------

def get_last_message(
    db: Session,
    chat_id: int,
) -> Optional[Message]:

    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .first()
    )


# ---------------------------------------------------------
# Update Message
# ---------------------------------------------------------

def update_message(
    db: Session,
    message_id: int,
    new_content: str,
) -> Optional[Message]:

    message = get_message(db, message_id)

    if message is None:
        return None

    message.content = new_content

    db.commit()
    db.refresh(message)

    return message


# ---------------------------------------------------------
# Delete Message
# ---------------------------------------------------------

def delete_message(
    db: Session,
    message_id: int,
) -> bool:

    message = get_message(db, message_id)

    if message is None:
        return False

    db.delete(message)

    db.commit()

    return True


# ---------------------------------------------------------
# Delete All Messages of Chat
# ---------------------------------------------------------

def delete_chat_messages(
    db: Session,
    chat_id: int,
):

    (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .delete()
    )

    db.commit()


# ---------------------------------------------------------
# Count Messages
# ---------------------------------------------------------

def message_count(
    db: Session,
    chat_id: int,
) -> int:

    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .count()
    )


# ---------------------------------------------------------
# User Messages
# ---------------------------------------------------------

def get_user_messages(
    db: Session,
    chat_id: int,
):

    return (
        db.query(Message)
        .filter(
            Message.chat_id == chat_id,
            Message.role == "user"
        )
        .order_by(Message.created_at.asc())
        .all()
    )


# ---------------------------------------------------------
# Assistant Messages
# ---------------------------------------------------------

def get_assistant_messages(
    db: Session,
    chat_id: int,
):

    return (
        db.query(Message)
        .filter(
            Message.chat_id == chat_id,
            Message.role == "assistant"
        )
        .order_by(Message.created_at.asc())
        .all()
    )