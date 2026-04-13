from sqlalchemy.orm import Session
from app.models import DefaultChore


def get_all_default_chores(db: Session) -> list[DefaultChore]:
    """Return all default chores ordered by position then id."""
    return db.query(DefaultChore).order_by(DefaultChore.position, DefaultChore.id).all()


def create_default_chore(db: Session, content: str) -> DefaultChore:
    """Add a new default chore to the global list."""
    chore = DefaultChore(content=content)
    db.add(chore)
    db.commit()
    db.refresh(chore)
    return chore


def delete_default_chore(db: Session, chore_id: int) -> None:
    """Remove a default chore by id. Does nothing if it doesn't exist."""
    chore = db.query(DefaultChore).filter(DefaultChore.id == chore_id).first()
    if chore:
        db.delete(chore)
        db.commit()
