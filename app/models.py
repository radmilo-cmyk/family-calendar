from sqlalchemy import Column, Integer, String, Date, Boolean, Time, ForeignKey
from app.database import Base


class Recurrence(Base):
    __tablename__ = "recurrences"

    id = Column(Integer, primary_key=True, index=True)
    frequency = Column(String, nullable=False)  # 'daily' | 'weekly' | 'monthly'
    days_of_week = Column(String, nullable=True)  # JSON array e.g. "[0,2]"; only for weekly
    start_date = Column(Date, nullable=False)
    until_date = Column(Date, nullable=False)
    excluded_dates = Column(String, nullable=False, default="[]")  # JSON array of YYYY-MM-DD
    content = Column(String, nullable=False)
    author = Column(String, nullable=False)
    time_start = Column(Time, nullable=True)
    time_end = Column(Time, nullable=True)


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String, nullable=False)
    done = Column(Boolean, default=False, nullable=False)
    done_by = Column(String, nullable=True)
    carried_over = Column(Boolean, default=False, nullable=False)
    original_date = Column(Date, nullable=True)
    time_start = Column(Time, nullable=True)
    time_end = Column(Time, nullable=True)
    recurrence_id = Column(Integer, ForeignKey("recurrences.id"), nullable=True)
    is_exception = Column(Integer, default=0, nullable=False)


class DefaultChore(Base):
    # Global list of chores that appear on every day view automatically.
    __tablename__ = "default_chores"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    # Controls display order (lower = first).
    sort_order = Column(Integer, default=0, nullable=False)
