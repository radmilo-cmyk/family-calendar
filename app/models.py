from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class Entry(Base):
    # This tells SQLAlchemy which table in the database this class maps to.
    __tablename__ = "entries"

    # Each Column() call defines one column in the table.
    # Integer primary_key=True means SQLite auto-assigns a unique number to each row.
    id = Column(Integer, primary_key=True, index=True)

    # The date the entry belongs to (stored as a date, not datetime — no time needed).
    date = Column(Date, nullable=False, index=True)

    # One of: "event", "chore", "message"
    type = Column(String, nullable=False)

    # The text the user typed in.
    content = Column(String, nullable=False)

    # The username of whoever created this entry (from the session).
    author = Column(String, nullable=False)
