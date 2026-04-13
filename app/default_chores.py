from sqlalchemy.orm import Session
from app.models import DefaultChore

# In-memory cache — default chores rarely change so we avoid a Supabase
# round-trip on every day view load and every toggle. Invalidated whenever
# the list is mutated (add or remove).
_cache: list[DefaultChore] | None = None


def _invalidate():
    global _cache
    _cache = None


def get_all_default_chores(db: Session) -> list[DefaultChore]:
    """Return all default chores ordered by position then id. Uses in-memory cache."""
    global _cache
    if _cache is None:
        _cache = db.query(DefaultChore).order_by(DefaultChore.position, DefaultChore.id).all()
    return _cache


def create_default_chore(db: Session, content: str) -> DefaultChore:
    """Add a new default chore to the global list."""
    chore = DefaultChore(content=content)
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
