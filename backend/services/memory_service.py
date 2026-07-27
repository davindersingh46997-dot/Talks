from sqlalchemy.orm import Session

from backend.crud.message import (
    create_message,
    get_chat_messages,
    get_last_message
)


class MessageService:

    @staticmethod
    def add_message(
        db: Session,
        chat_id: int,
        role: str,
        content: str
    ):

        return create_message(
            db=db,
            chat_id=chat_id,
            role=role,
            content=content
        )


    @staticmethod
    def get_messages(
        db: Session,
        chat_id: int
    ):

        return get_chat_messages(
            db,
            chat_id
        )


    @staticmethod
    def last_message(
        db: Session,
        chat_id: int
    ):

        return get_last_message(
            db,
            chat_id
        )