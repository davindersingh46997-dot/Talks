from backend.services.chat_service import chat
from backend.core.database import SessionLocal

db = SessionLocal()

res = chat(
    question="What is the capital of France?",
    chat_id=25,
    user_id=1,
    db=db
)

print(res)