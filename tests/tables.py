from backend.services.history_service import save_ai_message
from backend.core.database import SessionLocal

db = SessionLocal()

try:
    result = save_ai_message(
        db=db,
        chat_id=30,
        content="Paris is the capital of France.",
    )

    print("AI MESSAGE CREATED:", result.id)

finally:
    db.close()