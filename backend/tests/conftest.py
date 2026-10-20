import os


os.environ.setdefault("HF_TOKEN", "pytest-no-token")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "pytest")
os.environ.setdefault("DB_USER", "pytest")
os.environ.setdefault("DB_PASSWORD", "pytest")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg2://pytest:pytest@localhost:5432/pytest",
)
os.environ.setdefault("SECRET_KEY", "pytest-secret-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
