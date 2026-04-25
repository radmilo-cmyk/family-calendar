"""
Tests for event time slot functionality.

Covers: creating timed/all-day events, chore time field enforcement,
day view sort order, editing time slots, and clearing a time slot.
"""
from datetime import date, time

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Entry
from app.entries import create_entry, update_entry, get_entries_for_date


TODAY = date(2026, 4, 25)


@pytest.fixture()
def db():
    """Fresh in-memory SQLite DB for each test."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


# ---------------------------------------------------------------------------
# Task 7.1 — create event with time slot stored correctly
# ---------------------------------------------------------------------------

def test_create_event_with_time_slot(db):
    entry = create_entry(
        db,
        day=TODAY,
        entry_type="event",
        content="Dentist",
        author="user",
        time_start=time(9, 0),
        time_end=time(10, 0),
    )
    assert entry.time_start == time(9, 0)
    assert entry.time_end == time(10, 0)


def test_create_event_with_start_only(db):
    entry = create_entry(
        db,
        day=TODAY,
        entry_type="event",
        content="Meeting",
        author="user",
        time_start=time(14, 30),
    )
    assert entry.time_start == time(14, 30)
    assert entry.time_end is None


def test_create_all_day_event(db):
    entry = create_entry(
        db,
        day=TODAY,
        entry_type="event",
        content="Grandma birthday",
        author="user",
    )
    assert entry.time_start is None
    assert entry.time_end is None


# ---------------------------------------------------------------------------
# Task 7.2 — create chore always stores NULL time fields
# ---------------------------------------------------------------------------

def test_create_chore_time_fields_always_null(db):
    entry = create_entry(
        db,
        day=TODAY,
        entry_type="chore",
        content="Clean kitchen",
        author="user",
        time_start=time(9, 0),
        time_end=time(10, 0),
    )
    assert entry.time_start is None
    assert entry.time_end is None


def test_create_message_time_fields_always_null(db):
    entry = create_entry(
        db,
        day=TODAY,
        entry_type="message",
        content="Don't forget keys",
        author="user",
        time_start=time(8, 0),
    )
    assert entry.time_start is None
    assert entry.time_end is None


# ---------------------------------------------------------------------------
# Task 7.3 — day view sort: all-day first, then timed by time_start
# ---------------------------------------------------------------------------

def test_day_view_sort_order(db):
    create_entry(db, day=TODAY, entry_type="event", content="Late event",
                 author="u", time_start=time(16, 30))
    create_entry(db, day=TODAY, entry_type="event", content="All day 1",
                 author="u")
    create_entry(db, day=TODAY, entry_type="event", content="Early event",
                 author="u", time_start=time(9, 0))
    create_entry(db, day=TODAY, entry_type="event", content="All day 2",
                 author="u")

    entries = get_entries_for_date(db, TODAY)
    events_raw = [e for e in entries if e.type == "event"]
    events = sorted(events_raw, key=lambda e: (e.time_start is not None, e.time_start or time.min))

    assert events[0].content == "All day 1"
    assert events[1].content == "All day 2"
    assert events[2].content == "Early event"
    assert events[3].content == "Late event"


# ---------------------------------------------------------------------------
# Task 7.4 — edit event time slot updates correctly
# ---------------------------------------------------------------------------

def test_edit_event_updates_time_slot(db):
    entry = create_entry(
        db,
        day=TODAY,
        entry_type="event",
        content="Meeting",
        author="user",
        time_start=time(9, 0),
        time_end=time(10, 0),
    )
    update_entry(
        db,
        entry.id,
        content="Meeting updated",
        author="user",
        entry_type="event",
        time_start=time(11, 0),
        time_end=time(12, 0),
    )
    db.refresh(entry)
    assert entry.time_start == time(11, 0)
    assert entry.time_end == time(12, 0)


# ---------------------------------------------------------------------------
# Task 7.5 — clearing time on a timed event reverts it to all-day
# ---------------------------------------------------------------------------

def test_clear_time_reverts_to_all_day(db):
    entry = create_entry(
        db,
        day=TODAY,
        entry_type="event",
        content="Meeting",
        author="user",
        time_start=time(9, 0),
        time_end=time(10, 0),
    )
    update_entry(
        db,
        entry.id,
        content="Meeting",
        author="user",
        entry_type="event",
        time_start=None,
        time_end=None,
    )
    db.refresh(entry)
    assert entry.time_start is None
    assert entry.time_end is None
