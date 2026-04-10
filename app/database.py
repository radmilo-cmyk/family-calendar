import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Read DATABASE_URL from environment variable.
# - In production (Render): set DATABASE_URL to your Supabase PostgreSQL URI
# - In local dev: falls back to SQLite file if DATABASE_URL is not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./calendar.db")

# Supabase sometimes gives URLs starting with "postgres://" but SQLAlchemy
# requires "postgresql://" — this fixes that silently.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite needs an extra argument because FastAPI uses multiple threads.
# PostgreSQL handles this natively, so no extra args needed.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# A session factory — each request gets its own session (database conversation).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class that all our database models (tables) will inherit from.
class Base(DeclarativeBase):
    pass


def get_db():
    """
    FastAPI dependency that provides a database session per request.
    The 'yield' makes this a generator — FastAPI runs the code after yield
    when the request is finished, ensuring the session is always closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
