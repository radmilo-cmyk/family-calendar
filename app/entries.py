from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import extract

from app.models import Entry


def get_entries_for_date(db: Session, day: date) -> list[Entry]:
    """Return all entries for a specific date, ordered by id (insertion order)."""
    return db.query(Entry).filter(Entry.date == day).order_by(Entry.id).all()


def get_entries_for_range(db: Session, start: date, end: date) -> list[Entry]:
    """Return all entries between start and end dates (inclusive)."""
    return (
        db.query(Entry)
        .filter(Entry.date >= start, Entry.date <= end)
        .order_by(Entry.date, Entry.id)
        .all()
    )


def get_dates_with_entries(db: Session, year: int, month: int) -> set[date]:
    """
    Return a set of dates in the given month that have at least one entry.
    Used by the calendar view to mark which days have content.
    A set is used so the template can do fast 'date in dates_with_entries' checks.
    """
    rows = (
        db.query(Entry.date)
        .filter(
            extract("year", Entry.date) == year,
            extract("month", Entry.date) == month,
        )
        .distinct()
        .all()
    )
    # Each row is a tuple like (date(2026,4,3),), so we unpack with [0]
    return {row[0] for row in rows}


def create_entry(
    db: Session,
    day: date,
    entry_type: str,
    content: str,
    author: str,
) -> Entry:
    """Insert a new entry into the database and return it."""
    entry = Entry(date=day, type=entry_type, content=content, author=author)
    db.add(entry)
    db.commit()
    db.refresh(entry)  # reload from DB so entry.id is populated
    return entry


def get_entry(db: Session, entry_id: int) -> Entry | None:
    """Fetch a single entry by id, or None if it doesn't exist."""
    return db.query(Entry).filter(Entry.id == entry_id).first()


def delete_entry(db: Session, entry_id: int) -> None:
    """Hard-delete an entry. Does nothing if the id doesn't exist."""
    entry = get_entry(db, entry_id)
    if entry:
        db.delete(entry)
        db.commit()
