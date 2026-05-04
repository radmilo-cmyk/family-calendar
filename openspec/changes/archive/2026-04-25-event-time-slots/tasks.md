## 1. Database Migration

- [x] 1.1 Create `migrations/add_time_slots_to_entries.sql` with ALTER TABLE to add `time_start TIME DEFAULT NULL` and `time_end TIME DEFAULT NULL` to entries table
- [x] 1.2 Apply migration to local SQLite dev DB (DB was empty; model update creates tables with new columns on next app start)
- [x] 1.3 Apply migration to Supabase production DB

## 2. Backend — Model & Schema

- [x] 2.1 Add `time_start = Column(Time, nullable=True)` and `time_end = Column(Time, nullable=True)` to `Entry` model in `app/models.py`
- [x] 2.2 Update Pydantic create/update schemas in `app/entries.py` to include optional `time_start` and `time_end` fields
- [x] 2.3 Update create entry endpoint to store `time_start`/`time_end` only when `type == "event"` (force NULL otherwise)
- [x] 2.4 Update edit entry endpoint to accept and store `time_start`/`time_end` for event-type entries
- [x] 2.5 Update day entries query to sort by: `all-day first (time_start IS NULL), then time_start ASC`

## 3. Frontend — Create Form

- [x] 3.1 Add hidden time slot section to create form in `app/templates/day.html` with two `<input type="time">` fields (time_start, time_end)
- [x] 3.2 Add inline JS to show/hide time slot section when type selector changes to/from "event"
- [x] 3.3 Add client-side validation: if time_start set and time_end set, ensure time_end >= time_start

## 4. Frontend — Edit Form

- [x] 4.1 Add time slot fields to the inline edit form in `app/templates/day.html`
- [x] 4.2 Pre-fill time fields with existing entry values (from Jinja2 template context)
- [x] 4.3 Show/hide time slot section based on current entry type (JS on edit form type selector)

## 5. Frontend — Day View Display

- [x] 5.1 Add "All day" badge to event cards where `time_start` is NULL in `app/templates/day.html`
- [x] 5.2 Add time label (HH:MM – HH:MM or HH:MM) to event cards where `time_start` is set
- [x] 5.3 Verify day view renders all-day events above timed events (backend sort from 2.5)

## 6. Styling

- [x] 6.1 Style the "All day" badge consistent with existing design system (teal accent, small pill)
- [x] 6.2 Style time label (muted color, smaller font, same row as entry content)
- [x] 6.3 Style time slot picker section in create/edit forms (subtle, appears below content field)

## 7. Testing

- [x] 7.1 Write test: create event with time slot — stored correctly
- [x] 7.2 Write test: create chore — time fields are NULL regardless of input
- [x] 7.3 Write test: day view sort order — all-day events before timed events
- [x] 7.4 Write test: edit event — time slot updates correctly
- [x] 7.5 Write test: clear time on timed event — reverts to all-day
