from sqlalchemy import Column, Integer, String, Date, Boolean
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

    # Chore-specific: whether the chore is done and who did it.
    done = Column(Boolean, default=False, nullable=False)
    done_by = Column(String, nullable=True)

    # Carryover tracking: True when this entry was created by the midnight rollover job.
    carried_over = Column(Boolean, default=False, nullable=False)
    # The date the chore was first manually added (None for non-carried-over entries).
    original_date = Column(Date, nullable=True)


class DefaultChore(Base):
    # Global list of chores that appear on every day view automatically.
    __tablename__ = "default_chores"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    # Controls display order (lower = first).
    sort_order = Column(Integer, default=0, nullable=False)
