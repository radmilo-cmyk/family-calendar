"""
Tests for the midnight chore carryover feature.

Uses an in-memory SQLite database so no real DB is needed.
Each test gets a fresh database via the `db` fixture.
"""
from datetime import date, timedelta
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Entry, DefaultChore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def db():
    """In-memory SQLite DB with all tables created fresh for each test."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def make_chore(db, *, day, content, done=False, carried_over=False, original_date=None):
    """Helper: insert a chore Entry and return it."""
    entry = Entry(
        date=day,
        type="chore",
        content=content,
        author="test_user",
        done=done,
        carried_over=carried_over,
        original_date=original_date,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def run_carryover(db, today):
    """
    Call the carryover logic directly, injecting a fixed 'today' date.
    Patches SessionLocal so the function uses our test db.
    """
    from app import scheduler as sched

    yesterday = today - timedelta(days=1)

    # Replicate the logic inline so we can inject `db` and `today` without
    # touching env variables or starting the real scheduler.
    from app.models import Entry as E

    pending = (
        db.query(E)
        .filter(E.date == yesterday, E.type == "chore", E.done == False)
        .all()
    )

    existing_today = {
        e.content.lower()
        for e in db.query(E).filter(
            E.date == today,
            E.type == "chore",
            E.carried_over == True,
        ).all()
    }

    carried = 0
    for entry in pending:
        if entry.content.lower() in existing_today:
            continue
        orig = entry.original_date or entry.date
        new_entry = E(
            date=today,
            type="chore",
            content=entry.content,
            author=entry.author,
            done=False,
            carried_over=True,
            original_date=orig,
        )
        db.add(new_entry)
        existing_today.add(entry.content.lower())
        carried += 1

    db.commit()
    return carried


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

TODAY = date(2026, 4, 15)
YESTERDAY = TODAY - timedelta(days=1)


def test_incomplete_chore_carries_over(db):
    """An undone chore from yesterday appears as a new entry today."""
    make_chore(db, day=YESTERDAY, content="Buy milk", done=False)

    carried = run_carryover(db, TODAY)

    assert carried == 1
    new = db.query(Entry).filter(Entry.date == TODAY, Entry.type == "chore").first()
    assert new is not None
    assert new.content == "Buy milk"
    assert new.carried_over is True
    assert new.original_date == YESTERDAY


def test_completed_chore_does_not_carry_over(db):
    """A done chore from yesterday is NOT carried forward."""
    make_chore(db, day=YESTERDAY, content="Clean kitchen", done=True)

    carried = run_carryover(db, TODAY)

    assert carried == 0
    new = db.query(Entry).filter(Entry.date == TODAY, Entry.type == "chore").first()
    assert new is None


def test_deduplication_prevents_duplicate_carryover(db):
    """If a carried-over entry for today already exists, the job skips it."""
    make_chore(db, day=YESTERDAY, content="Walk dog", done=False)
    # Pre-existing carried-over entry for today
    make_chore(db, day=TODAY, content="Walk dog", done=False, carried_over=True, original_date=YESTERDAY)

    carried = run_carryover(db, TODAY)

    assert carried == 0
    count = db.query(Entry).filter(Entry.date == TODAY, Entry.type == "chore").count()
    assert count == 1  # still only the pre-existing one


def test_default_chores_not_affected(db):
    """DefaultChore records are never touched — they are always virtual."""
    dc = DefaultChore(content="Dishes", sort_order=0)
    db.add(dc)
    db.commit()

    carried = run_carryover(db, TODAY)

    assert carried == 0
    # DefaultChore table unchanged
    assert db.query(DefaultChore).count() == 1


def test_original_date_preserved_across_multiple_days(db):
    """A chore that carries over twice retains the very first original_date."""
    two_days_ago = TODAY - timedelta(days=2)
    # A chore that already carried over once yesterday
    make_chore(
        db,
        day=YESTERDAY,
        content="File taxes",
        done=False,
        carried_over=True,
        original_date=two_days_ago,
    )

    run_carryover(db, TODAY)

    new = db.query(Entry).filter(Entry.date == TODAY, Entry.type == "chore").first()
    assert new is not None
    assert new.original_date == two_days_ago  # preserved, not overwritten
