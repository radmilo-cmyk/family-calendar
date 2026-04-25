from datetime import time


def parse_time(value: str | None) -> time | None:
    """Parse an HH:MM string from a form time input. Returns None for empty/invalid input."""
    if not value or not value.strip():
        return None
    try:
        return time.fromisoformat(value.strip())
    except ValueError:
        return None
