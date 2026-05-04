## Context

The app stores calendar entries (events, chores, messages) per date in a SQLite database. Events can have a time slot. Currently every entry is independent — there is no concept of a series. This design introduces recurring events: a rule that causes an event to appear on multiple dates without manual re-entry.

## Goals / Non-Goals

**Goals:**
- Store a recurrence rule once; surface instances across the calendar without storing a row per occurrence
- Support: daily, weekly (any subset of days), monthly (same day-of-month)
- Support an `until` date to bound the series
- Allow editing or deleting a single occurrence without affecting the rest of the series
- Allow editing or deleting all future occurrences from a given date

**Non-Goals:**
- Recurrence for chores or messages (events only for now)
- Complex iCal RRULE patterns (bi-weekly, nth weekday of month, count-based limits)
- Syncing with external calendars

## Decisions

### 1. Rule-based storage with on-the-fly expansion (not row-per-occurrence)

**Decision**: Store one recurrence rule; compute which dates it applies to at query time.

**Why**: A family app rarely has hundreds of events. On-the-fly expansion keeps the DB small, avoids the need to bulk-generate rows on create, and makes editing the rule (change until date, change days) simple — one row update.

**Alternative considered**: Pre-expand and store a row per occurrence. Simpler queries, but creates N rows on create, requires bulk updates on edit, and wastes space for rules with long `until` dates.

### 2. Exception model for "edit/delete this occurrence only"

**Decision**: When a user edits or deletes a single occurrence, record that date as an **exception** against the recurrence rule. For edits, also create a standalone entry for that date with the modified content. For deletes, just record the excluded date.

**Why**: The recurrence rule remains the source of truth. Exceptions are rare and naturally represented as a small list of excluded dates on the rule record.

**Data shape**:
```
recurrences table:
  id            INTEGER PK
  frequency     TEXT  -- 'daily' | 'weekly' | 'monthly'
  days_of_week  TEXT  -- JSON array e.g. [1,3,5]  (0=Mon…6=Sun); null for daily/monthly
  until_date    TEXT  -- YYYY-MM-DD
  excluded_dates TEXT -- JSON array of YYYY-MM-DD strings (skipped occurrences)
  content       TEXT  -- event text for all instances
  author        TEXT
  time_start    TEXT  -- nullable HH:MM
  time_end      TEXT  -- nullable HH:MM

entries table (additions):
  recurrence_id INTEGER REFERENCES recurrences(id) -- null for standalone entries
  is_exception  INTEGER DEFAULT 0                  -- 1 = this row overrides a recurrence occurrence
```

### 3. "Edit all future" splits the rule

**Decision**: Editing all occurrences from date D onward truncates the existing rule's `until_date` to D-1 and creates a new rule starting at D with the updated values.

**Why**: Simple to reason about. Old occurrences remain unchanged. New rule is a first-class citizen with its own exceptions list.

### 4. API shape

New endpoints:
- `POST /recurrences` — create a recurrence rule; returns rule id
- `PUT /recurrences/<id>` — edit all future (may split)
- `DELETE /recurrences/<id>` — delete all future occurrences from a date (may split or fully delete)
- `POST /recurrences/<id>/exceptions` — add an excluded date (delete this occurrence)

Existing endpoints:
- `GET /entries/<date>` — updated to also return computed recurrence instances for that date
- `POST /entries` — gains optional `recurrence` payload to create a recurring event
- `PUT /entries/<id>` — if entry has `recurrence_id` and `is_exception=0`, backend asks frontend to choose scope (this / all future) before proceeding

### 5. Frontend recurrence picker

A collapsible "Repeat" section in the event creation and edit forms:
- Toggle: off / on
- Frequency: Daily / Weekly / Monthly
- Days of week (multi-select, shown only for Weekly)
- Until date (date picker)

Edit/delete of a recurring entry shows a scope modal: "This event" vs "This and all future events."

## Risks / Trade-offs

- [Risk: On-the-fly expansion is slow for long rules] → Expansion is bounded by the displayed date range (one month at a time). With a typical family calendar (< 10 recurrences), this is negligible.
- [Risk: Exception list grows unbounded if user deletes many occurrences] → Acceptable for a personal/family app. Could add a cleanup job later.
- [Risk: Split-rule approach duplicates data across two rule rows] → Trade-off for simplicity. Content edits on "all future" require updating both new rule content and exceptions on the old rule. Document this clearly in code.

## Migration Plan

1. Add `recurrences` table (new migration, non-destructive)
2. Add nullable `recurrence_id` and `is_exception` columns to `entries` (ALTER TABLE, backward compatible)
3. Deploy backend with new endpoints; existing entry endpoints remain unchanged for standalone entries
4. Deploy frontend with recurrence picker (hidden behind new UI — no forced migration)
5. No data migration needed — all existing entries remain standalone (`recurrence_id = NULL`)
