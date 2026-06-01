## Why

The monthly calendar grid shows dots on dates with events, but gives no quick overview of what's coming up. Users have to tap each day individually to find upcoming events — an agenda list below the calendar makes the next few days scannable at a glance.

## What Changes

- Add a read-only agenda strip below the monthly calendar grid on the home page
- Shows events only (not chores or messages) from today forward within the viewed month
- Each row: date on the left, event title(s) and time on the right
- Clicking a row navigates to that day's view (same as tapping a day in the grid)
- If viewing a future month, all dates with events in that month are shown
- No inline editing — the list is purely for scanning

## Capabilities

### New Capabilities
- `home-agenda-list`: Read-only agenda strip below the calendar grid showing upcoming events grouped by date

### Modified Capabilities
- `calendar-view`: Home page now includes an agenda list section below the grid (new rendered section, no requirement removals)

## Impact

- `app/entries.py` — new query function `get_month_events_from_today()`
- `app/main.py` — pass grouped events dict to calendar template
- `app/templates/calendar.html` — new agenda section below `</table>`
- `app/static/style.css` — agenda list styles matching existing design system
