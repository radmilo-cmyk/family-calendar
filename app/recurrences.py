import json
from dataclasses import dataclass, field
from datetime import date, time as time_type, timedelta
from calendar import monthrange
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Recurrence, Entry


# ---------------------------------------------------------------------------
# Virtual entry dataclass — mimics Entry for template use
# ---------------------------------------------------------------------------

@dataclass
class RecurrenceInstance:
    recurrence_id: int
    date: date
    content: str
    author: str
    time_start: Optional[time_type]
    time_end: Optional[time_type]
    id: None = None
    type: str = "event"
    done: bool = False
    done_by: None = None
    carried_over: bool = False
    original_date: None = None
    is_exception: int = 0
    is_recurring_instance: bool = True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_json_list(value: Optional[str]) -> list:
    if not value:
        return []
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []


def _dump_json_list(lst: list) -> str:
    return json.dumps(lst)


def _matches_rule(rule: Recurrence, day: date) -> bool:
    """Return True if `day` is a valid occurrence of `rule`."""
    if day < rule.start_date or day > rule.until_date:
        return False
    excluded = _load_json_list(rule.excluded_dates)
    if day.isoformat() in excluded:
        return False
    if rule.frequency == "daily":
        return True
    if rule.frequency == "weekly":
        dow = _load_json_list(rule.days_of_week)
        return day.weekday() in dow
    if rule.frequency == "monthly":
        return day.day == rule.start_date.day
    return False


def _rule_to_instance(rule: Recurrence, day: date) -> RecurrenceInstance:
    return RecurrenceInstance(
        recurrence_id=rule.id,
        date=day,
        content=rule.content,
        author=rule.author,
        time_start=rule.time_start,
        time_end=rule.time_end,
    )


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def create_recurrence(
    db: Session,
    frequency: str,
    start_date: date,
    until_date: date,
    content: str,
    author: str,
    days_of_week: Optional[list] = None,
    time_start: Optional[time_type] = None,
    time_end: Optional[time_type] = None,
) -> Recurrence:
    rule = Recurrence(
        frequency=frequency,
        days_of_week=_dump_json_list(days_of_week or []) if frequency == "weekly" else None,
        start_date=start_date,
        until_date=until_date,
        excluded_dates="[]",
        content=content,
        author=author,
        time_start=time_start,
        time_end=time_end,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def get_recurrence(db: Session, rule_id: int) -> Optional[Recurrence]:
    return db.query(Recurrence).filter(Recurrence.id == rule_id).first()


def get_all_active_rules(db: Session, as_of: date) -> list[Recurrence]:
    """Rules still active on or after `as_of`."""
    return db.query(Recurrence).filter(Recurrence.until_date >= as_of).all()


# ---------------------------------------------------------------------------
# Exception (delete this occurrence)
# ---------------------------------------------------------------------------

def add_exception_date(db: Session, rule_id: int, exc_date: date) -> None:
    rule = get_recurrence(db, rule_id)
    if not rule:
        return
    excluded = _load_json_list(rule.excluded_dates)
    iso = exc_date.isoformat()
    if iso not in excluded:
        excluded.append(iso)
        rule.excluded_dates = _dump_json_list(excluded)
        db.commit()


# ---------------------------------------------------------------------------
# Delete all future occurrences from a date
# ---------------------------------------------------------------------------

def delete_from_date(db: Session, rule_id: int, from_date: date) -> None:
    rule = get_recurrence(db, rule_id)
    if not rule:
        return
    if from_date <= rule.start_date:
        # Deleting from the very beginning — remove the whole rule
        db.delete(rule)
    else:
        rule.until_date = from_date - timedelta(days=1)
    db.commit()


# ---------------------------------------------------------------------------
# Edit this occurrence (exception + standalone entry)
# ---------------------------------------------------------------------------

def edit_this_occurrence(
    db: Session,
    rule_id: int,
    exc_date: date,
    content: str,
    author: str,
    time_start: Optional[time_type] = None,
    time_end: Optional[time_type] = None,
) -> Entry:
    add_exception_date(db, rule_id, exc_date)
    entry = Entry(
        date=exc_date,
        type="event",
        content=content,
        author=author,
        time_start=time_start,
        time_end=time_end,
        recurrence_id=rule_id,
        is_exception=1,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


# ---------------------------------------------------------------------------
# Edit all future occurrences (split rule)
# ---------------------------------------------------------------------------

def edit_from_date(
    db: Session,
    rule_id: int,
    from_date: date,
    content: str,
    author: str,
    time_start: Optional[time_type] = None,
    time_end: Optional[time_type] = None,
) -> Recurrence:
    rule = get_recurrence(db, rule_id)
    if not rule:
        return None

    old_until = rule.until_date
    old_frequency = rule.frequency
    old_dow = _load_json_list(rule.days_of_week)

    if from_date <= rule.start_date:
        # Editing from the beginning — just update in-place
        rule.content = content
        rule.author = author
        rule.time_start = time_start
        rule.time_end = time_end
        db.commit()
        return rule

    # Truncate old rule
    rule.until_date = from_date - timedelta(days=1)
    db.commit()

    # Create new rule for from_date onward
    new_rule = create_recurrence(
        db,
        frequency=old_frequency,
        start_date=from_date,
        until_date=old_until,
        content=content,
        author=author,
        days_of_week=old_dow if old_frequency == "weekly" else None,
        time_start=time_start,
        time_end=time_end,
    )
    return new_rule


# ---------------------------------------------------------------------------
# Expansion
# ---------------------------------------------------------------------------

def instances_for_date(db: Session, day: date) -> list[RecurrenceInstance]:
    """Return virtual recurring instances that fall on `day`."""
    rules = get_all_active_rules(db, as_of=day)
    return [_rule_to_instance(r, day) for r in rules if _matches_rule(r, day)]


def instances_for_range(db: Session, start: date, end: date) -> list[RecurrenceInstance]:
    """Return all virtual recurring instances in [start, end]."""
    rules = get_all_active_rules(db, as_of=start)
    # Only consider rules whose until_date overlaps the range
    relevant = [r for r in rules if r.until_date >= start]
    results = []
    delta = (end - start).days
    for i in range(delta + 1):
        day = start + timedelta(days=i)
        for r in relevant:
            if _matches_rule(r, day):
                results.append(_rule_to_instance(r, day))
    return results


def dates_with_instances_for_month(db: Session, year: int, month: int) -> set[date]:
    """Return the set of dates in the month that have at least one recurring instance."""
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    instances = instances_for_range(db, first_day, last_day)
    return {inst.date for inst in instances}
