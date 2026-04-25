## Context

The `Entry` model stores `date` (Date) but no time information. All entries are treated as full-day. The day view renders entries in insertion order. The create and edit forms have no time picker. No migration infrastructure currently exists — past migrations are raw SQL files applied manually.

The app is a FastAPI + SQLAlchemy backend with Jinja2 HTML templates. Frontend is vanilla JS (no framework). DB is SQLite in dev, PostgreSQL (Supabase) in production. Both support nullable `TIME` columns natively.

## Goals / Non-Goals

**Goals:**
- Add `time_start` / `time_end` (nullable TIME) to the `Entry` model
- NULL = all-day; non-NULL = timed event
- Time picker appears in create form only for `type = event`
- Time picker appears in edit form for any event-type entry
- Day view sorts: all-day events first (with badge), then timed events by `time_start` ascending
- Existing entries migrated to NULL (all-day) automatically via SQL migration
- Only `event` type gets time slots — chores and messages remain untouched

**Non-Goals:**
- Multi-day spanning events
- Recurring/repeating events
- Calendar grid hour-by-hour timeline view
- Time zones (all times are local/naive)

## Decisions

### 1. Store as nullable TIME columns, not a boolean `all_day` flag

**Decision:** Two columns — `time_start TIME NULL`, `time_end TIME NULL`. All-day = both NULL.

**Why:** A dedicated flag would require keeping it in sync with time values. Null time columns are self-describing: NULL means no time, non-NULL means a time exists. Less surface area for bugs.

**Alternative considered:** Single `time_start` only (no `time_end`). Rejected because events have duration; end time is useful for display and future sorting.

### 2. Sort order: all-day events first, then timed events by time_start

**Decision:** In the entries list query (per day), sort by: `CASE WHEN time_start IS NULL THEN 0 ELSE 1 END ASC, time_start ASC NULLS FIRST`.

**Why:** All-day events are structural anchors for the day. Timed events are time-specific and should flow chronologically below them.

### 3. Time picker is HTML `<input type="time">` — no JS library

**Decision:** Use native browser time picker (`<input type="time">`). No external dependency.

**Why:** App currently has zero JS dependencies. Native time picker works on mobile (important — family uses phones). Keeps the codebase simple.

### 4. Time picker visibility toggled by JS on type selector change

**Decision:** The time slot section is hidden by default and revealed via a small inline JS snippet when `type === "event"` is selected.

**Why:** Chores and messages should never have time slots. Hiding the field avoids confusion and prevents accidental data entry.

### 5. Migration: raw SQL file, NULL default

**Decision:** Add `add_time_slots_to_entries.sql` that runs `ALTER TABLE entries ADD COLUMN time_start TIME DEFAULT NULL` and the same for `time_end`. Existing rows automatically get NULL (= all-day). No data transformation needed.

**Why:** NULL default is backwards-compatible. Both SQLite and PostgreSQL support this syntax. No downtime required.

## Risks / Trade-offs

- **`time_end` optional in form** → Users may set `time_start` without `time_end`. Backend accepts this (partial time is valid). Display shows "14:00 –" if no end time. Risk: visual inconsistency. Mitigation: form shows both fields together, JS validates end ≥ start client-side.
- **SQLite stores TIME as TEXT** → SQLite has no native TIME type; it stores as `"HH:MM:SS"` string. Sort works correctly as string comparison for `HH:MM` format. PostgreSQL handles it natively. Mitigation: store and retrieve as `"HH:MM"` strings; SQLAlchemy `Time` column handles coercion transparently.
- **Existing entries become all-day** → Users who embedded time in content text (e.g. "dentist 14:00") will need to manually re-enter time on those entries via edit. Mitigation: edit form is already functional; proposal note informs user.

## Migration Plan

1. Add `migrations/add_time_slots_to_entries.sql`
2. Run on SQLite dev DB: `sqlite3 calendar.db < migrations/add_time_slots_to_entries.sql`
3. Run on Supabase production DB via SQL editor or psql
4. Deploy new code after migration (or simultaneously — NULL default means old code still works on migrated DB)

**Rollback:** `ALTER TABLE entries DROP COLUMN time_start; ALTER TABLE entries DROP COLUMN time_end;` — safe since columns are NULL-only at rollback point.

## Open Questions

- Should `time_end` be required when `time_start` is set? (Current decision: no — optional.)
- Should chores ever get time slots in future? (Current decision: out of scope.)
