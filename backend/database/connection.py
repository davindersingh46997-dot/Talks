from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://username:password@localhost:5432/chatbot_db"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)