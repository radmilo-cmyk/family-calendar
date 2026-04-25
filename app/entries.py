from datetime import date, time as time_type
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
    time_start: time_type | None = None,
    time_end: time_type | None = None,
) -> Entry:
    """Insert a new entry into the database and return it."""
    entry = Entry(
        date=day,
        type=entry_type,
        content=content,
        author=author,
        time_start=time_start if entry_type == "event" else None,
        time_end=time_end if entry_type == "event" else None,
    )
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


def update_entry(
    db: Session,
    entry_id: int,
    content: str,
    author: str,
    entry_type: str,
    time_start: time_type | None = None,
    time_end: time_type | None = None,
) -> None:
    """Update content, author, type, and optional time slot of an existing entry."""
    entry = get_entry(db, entry_id)
    if entry:
        entry.content = content
        entry.author = author
        entry.type = entry_type
        entry.time_start = time_start if entry_type == "event" else None
        entry.time_end = time_end if entry_type == "event" else None
        db.commit()


def toggle_chore_done(db: Session, entry_id: int, current_user: str) -> None:
    """Flip a chore's done state. If undone → done (record who did it). If done → undone."""
    entry = get_entry(db, entry_id)
    if entry and entry.type == "chore":
        if entry.done:
            entry.done = False
            entry.done_by = None
        else:
            entry.done = True
            entry.done_by = current_user
        db.commit()


def complete_virtual_default(db: Session, day: date, content: str, current_user: str) -> Entry:
    """Create a chore entry for a default chore and immediately mark it done."""
    entry = Entry(
        date=day,
        type="chore",
        content=content,
        author=current_user,
        done=True,
        done_by=current_user,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
