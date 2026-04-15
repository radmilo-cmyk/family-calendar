from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import DefaultChore

# In-memory cache — default chores rarely change so we avoid a Supabase
# round-trip on every day view load and every toggle. Invalidated whenever
# the list is mutated (add, remove, or reorder).
_cache: list[DefaultChore] | None = None


def _invalidate():
    global _cache
    _cache = None


def get_all_default_chores(db: Session) -> list[DefaultChore]:
    """Return all default chores ordered by sort_order then id. Uses in-memory cache."""
    global _cache
    if _cache is None:
        _cache = db.query(DefaultChore).order_by(DefaultChore.sort_order, DefaultChore.id).all()
    return _cache


def create_default_chore(db: Session, content: str) -> DefaultChore:
    """Add a new default chore at the end of the list."""
    max_order = db.query(func.max(DefaultChore.sort_order)).scalar()
    next_order = (max_order + 1) if max_order is not None else 0
    chore = DefaultChore(content=content, sort_order=next_order)
    db.add(chore)
    db.commit()
    db.refresh(chore)
    _invalidate()
    return chore


def delete_default_chore(db: Session, chore_id: int) -> None:
    """Remove a default chore by id. Does nothing if it doesn't exist."""
    chore = db.query(DefaultChore).filter(DefaultChore.id == chore_id).first()
    if chore:
        db.delete(chore)
        db.commit()
        _invalidate()


def reorder_default_chores(db: Session, ids: list[int]) -> None:
    """Update sort_order for all default chores based on the provided id order."""
    for i, chore_id in enumerate(ids):
        db.query(DefaultChore).filter(DefaultChore.id == chore_id).update({"sort_order": i})
    db.commit()
    _invalidate()
