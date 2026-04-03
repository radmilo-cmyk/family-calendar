from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite stores everything in a single file — "calendar.db" in the project root.
# The three slashes mean a relative path: sqlite:///./calendar.db
DATABASE_URL = "sqlite:///./calendar.db"

# The engine is the low-level connection to the database file.
# check_same_thread=False is needed because FastAPI handles requests across threads.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

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
