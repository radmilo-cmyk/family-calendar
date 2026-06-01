## 1. Backend — Query Function

- [x] 1.1 Add `get_month_events_from_today(db, year, month)` to `app/entries.py` — queries all Event entries for the given month, filters to `date >= today` when month is current, skips entirely for past months, returns `dict[date, list[Entry]]` sorted by date ascending

## 2. Backend — Route

- [x] 2.1 In `calendar_root` in `app/main.py`, call `get_month_events_from_today` and pass the result as `agenda_events` to the `calendar.html` template context

## 3. Frontend — Template

- [x] 3.1 In `app/templates/calendar.html`, add an agenda section below `</table>` that renders only when `agenda_events` is non-empty
- [x] 3.2 Iterate `agenda_events.items()` to render each date as a clickable row linking to `/day/YYYY-MM-DD`
- [x] 3.3 For each event under a date, show content and time label (`HH:MM – HH:MM` or `HH:MM` or nothing for all-day)

## 4. Frontend — Styles

- [x] 4.1 Add agenda list CSS to `app/static/style.css` using existing design tokens (`--color-primary`, `--color-border`, `--color-bg`, `--radius`, `Quicksand` font) — card style matching the rest of the app
- [x] 4.2 Ensure mobile layout is correct at 320px: full width, no overflow, text truncation with ellipsis on long titles

## 5. Verification

- [x] 5.1 Start the dev server and verify agenda appears below the grid on the current month with at least one future event
- [x] 5.2 Verify agenda is hidden when navigating to a month with no upcoming events
- [x] 5.3 Verify clicking an agenda row navigates to the correct day view
- [x] 5.4 Verify no edit/delete controls appear in the agenda section
