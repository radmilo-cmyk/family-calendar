from datetime import date, time as time_type
from sqlalchemy.orm import Session
from sqlalchemy import extract

from app.models import Entry


def get_entries_for_date(db: Session, day: date) -> list:
    """Return all entries for a date, including recurring instances."""
    from app.recurrences import instances_for_date
    stored = db.query(Entry).filter(Entry.date == day).order_by(Entry.id).all()
    recurring = instances_for_date(db, day)
    return stored + recurring


def get_entries_for_range(db: Session, start: date, end: date) -> list:
    """Return all entries in [start, end], including recurring instances."""
    from app.recurrences import instances_for_range
    stored = (
        db.query(Entry)
        .filter(Entry.date >= start, Entry.date <= end)
        .order_by(Entry.date, Entry.id)
        .all()
    )
    recurring = instances_for_range(db, start, end)
    combined = sorted(stored + recurring, key=lambda e: (e.date, getattr(e, 'id', float('inf')) or float('inf')))
    return combined


def get_dates_with_entries(db: Session, year: int, month: int) -> set[date]:
    """Return dates in the month that have at least one entry or recurring instance."""
    from app.recurrences import dates_with_instances_for_month
    rows = (
        db.query(Entry.date)
        .filter(
            extract("year", Entry.date) == year,
            extract("month", Entry.date) == month,
        )
        .distinct()
        .all()
    )
    stored_dates = {row[0] for row in rows}
    recurring_dates = dates_with_instances_for_month(db, year, month)
    return stored_dates | recurring_dates


def get_upcoming_events(db: Session, page: int = 0, page_size: int = 5) -> tuple:
    """Return upcoming events grouped by date, paginated by date group.

    Includes both stored entries and virtual recurring instances.
    Returns (agenda_events: dict[date, list], has_prev: bool, has_next: bool).
    """
    from datetime import date as date_type, timedelta
    from datetime import time as time_type
    from app.recurrences import instances_for_range

    today = date_type.today()
    horizon = today + timedelta(days=365)

    stored = (
        db.query(Entry)
        .filter(Entry.type == "event", Entry.date >= today, Entry.date <= horizon)
        .all()
    )
    # Exception dates are already excluded from recurring instances via excluded_dates,
    # so stored exception entries and virtual instances never overlap.
    recurring = instances_for_range(db, today, horizon)

    all_entries = stored + recurring
    all_entries.sort(key=lambda e: (e.date, e.time_start is not None, e.time_start or time_type.min))

    grouped: dict = {}
    for entry in all_entries:
        grouped.setdefault(entry.date, []).append(entry)

    all_dates = list(grouped.keys())
    start = page * page_size
    end = start + page_size
    page_dates = all_dates[start:end]

    return (
        {d: grouped[d] for d in page_dates},
        page > 0,
        end < len(all_dates),
    )


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
