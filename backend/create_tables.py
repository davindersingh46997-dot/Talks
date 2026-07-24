from backend.core.database import Base
from backend.core.database import engine

# Import all models
from backend.models import User
from backend.models import Chat
from backend.models import Message

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Done!")