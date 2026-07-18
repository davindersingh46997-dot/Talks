from collections import defaultdict
from typing import List

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    BaseMessage,
)


class ShortTermMemory:
    """
    Stores conversation history for each session.

    session_id
        chat_1
            Human
            AI
            Human
            AI

        chat_2
            Human
            AI
    """

    def __init__(self, max_messages: int = 20):

        self.max_messages = max_messages

        self._memory = defaultdict(list)

    # -----------------------------
    # Add Messages
    # -----------------------------

    def add_user_message(
        self,
        session_id: str,
        message: str,
    ):

        self._memory[session_id].append(
            HumanMessage(content=message)
        )

        self._trim(session_id)

    def add_ai_message(
        self,
        session_id: str,
        message: str,
    ):

        self._memory[session_id].append(
            AIMessage(content=message)
        )

        self._trim(session_id)

    # -----------------------------
    # Retrieve Memory
    # -----------------------------

    def get_messages(
        self,
        session_id: str,
    ) -> List[BaseMessage]:

        return list(self._memory[session_id])

    # -----------------------------
    # Clear Memory
    # -----------------------------

    def clear(
        self,
        session_id: str,
    ):

        self._memory[session_id] = []

    # -----------------------------
    # Delete Session
    # -----------------------------

    def delete_session(
        self,
        session_id: str,
    ):

        if session_id in self._memory:

            del self._memory[session_id]

    # -----------------------------
    # List Sessions
    # -----------------------------

    def sessions(self):

        return list(self._memory.keys())

    # -----------------------------
    # Internal Helper
    # -----------------------------

    def _trim(
        self,
        session_id: str,
    ):

        """
        Keep only the most recent messages.
        """

        if len(self._memory[session_id]) > self.max_messages:

            self._memory[session_id] = self._memory[
                session_id
            ][-self.max_messages:]