from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/chat_db"

test_engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

db = TestSessionLocal()

db.close()

