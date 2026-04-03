import calendar
from datetime import date


def build_month_grid(year: int, month: int) -> list[list[date | None]]:
    """
    Return the month as a list of weeks.
    Each week is a list of 7 items: a date object or None (for padding days).

    Example for April 2026 (starts on Wednesday):
    [
      [None, None, None, date(2026,4,1), date(2026,4,2), date(2026,4,3), date(2026,4,4)],
      [date(2026,4,5), ...],
      ...
    ]
    """
    # calendar.monthcalendar returns 0 for days outside the month.
    raw = calendar.monthcalendar(year, month)

    grid = []
    for week in raw:
        row = []
        for day_num in week:
            if day_num == 0:
                row.append(None)      # padding — not a real day in this month
            else:
                row.append(date(year, month, day_num))
        grid.append(row)

    return grid


def get_year_month(year: int, month: int, delta: int) -> tuple[int, int]:
    """
    Return the year and month after adding `delta` months.
    delta=+1 gives next month, delta=-1 gives previous month.
    """
    month += delta
    if month > 12:
        month = 1
        year += 1
    elif month < 1:
        month = 12
        year -= 1
    return year, month
