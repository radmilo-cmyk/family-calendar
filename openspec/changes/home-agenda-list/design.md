## Context

The home page (`/`) renders a monthly calendar grid via `calendar.html`. The backend sends `dates_with_entries` (a set of dates) to power the dot indicators on cells. No entry content is passed to the calendar template today — only presence/absence per date.

The design system uses CSS variables (teal palette, `Quicksand` body font, `Caveat` headings, `--radius: 12px`, `--shadow-sm`). All rendering is server-side via Jinja2. There is no client-side JS data fetching in this app.

## Goals / Non-Goals

**Goals:**
- Render a read-only agenda list below the calendar grid showing upcoming events in the viewed month
- Pass grouped event data from the backend in one new query (no N+1 per date)
- Match existing visual design system exactly (fonts, colors, card style, spacing)

**Non-Goals:**
- Inline editing from the agenda list
- Showing chores or messages
- Showing events across month boundaries or multi-month lookahead
- Pagination or lazy loading
- Any JavaScript / AJAX

## Decisions

### 1. Single new DB query function, not N+1 per date

**Decision**: Add `get_month_events_from_today(db, year, month)` that fetches all event entries for the month in one query, filtered to `date >= today` when viewing the current month.

**Why**: The existing `get_entries_for_date` fetches one date at a time. Calling it for every date with entries would be N queries per page load. A single query is more efficient and keeps the route simple.

**Alternative considered**: Reuse existing function in a loop. Rejected — unnecessary DB round trips.

### 2. Pass `agenda_events` dict to template, not a flat list

**Decision**: The route passes `agenda_events: dict[date, list[Entry]]` — dates as keys, ordered lists of Entry objects as values. Dates are sorted ascending.

**Why**: The template can iterate `agenda_events.items()` directly to render grouped rows. Sorting and grouping in Python keeps the template logic minimal.

### 3. Recurring events included via existing recurrence expansion

**Decision**: The query fetches only `Entry` rows (standalone + exception overrides). Recurring virtual instances are **not** included in the agenda list.

**Why**: Recurring instances are not stored as `Entry` rows — they are virtual, computed per day view. Expanding them for a full month in the home route would require the recurrence engine and adds complexity. The calendar dot already shows recurring days; the agenda focuses on explicitly added events.

**Revisit if**: Users find the agenda confusing because recurring events don't appear in it.

### 4. Agenda section hidden when empty

**Decision**: If `agenda_events` is empty (no upcoming events in the month), the agenda section is not rendered at all.

**Why**: An empty "Upcoming" header with nothing below it adds visual noise with no value.

## Risks / Trade-offs

- [Recurring events missing from agenda] → Mitigated by existing dot indicators on the grid; document as known limitation
- [Long event title overflows on mobile] → Mitigate with `text-overflow: ellipsis` and `max-width` on the content cell
- [Many events making the page very long] → Acceptable for a family calendar; no pagination needed at this scale

## Migration Plan

No schema changes. No data migration. Pure addition of a query function, a route dict key, and a template section. Rollback = revert those three changes.
