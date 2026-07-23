from langchain_core.messages import HumanMessage, AIMessage


class ShortTermMemory:
    def __init__(self,max_messages=20):
        self.sessions = {}
        self.max_messages = max_messages

    def get_messages(self, session_id: str):
        return self.sessions.get(session_id, [])

    def add_user_message(self, session_id: str, message: str):

        messages = self.sessions.setdefault(session_id, [])

        messages.append(HumanMessage(content=message))

        if len(messages) > self.max_messages:
            messages.pop(0)

    def add_ai_message(self, session_id: str, message: str):

        messages = self.sessions.setdefault(session_id, [])

        messages.append(AIMessage(content=message))
        
        if len(messages) > self.max_messages:
            messages.pop(0)

    def clear(self, session_id: str):
        self.sessions[session_id] = []

        