## 1. Database Migration

- [x] 1.1 Create `recurrences` table migration (frequency, days_of_week, until_date, excluded_dates, content, author, time_start, time_end)
- [x] 1.2 Add `recurrence_id` (nullable FK) and `is_exception` (integer default 0) columns to `entries` table

## 2. Backend — Recurrence API

- [x] 2.1 Create `POST /recurrences` endpoint to create a recurrence rule
- [x] 2.2 Create `PUT /recurrences/<id>` endpoint to edit all future occurrences (splits rule at given date)
- [x] 2.3 Create `DELETE /recurrences/<id>` endpoint to delete all future occurrences (updates until_date or hard-deletes)
- [x] 2.4 Create `POST /recurrences/<id>/exceptions` endpoint to add an excluded date (delete this occurrence)

## 3. Backend — Entry Query Updates

- [x] 3.1 Add recurrence expansion logic: given a date, compute which rules produce an instance (checks frequency, days_of_week, until_date, excluded_dates)
- [x] 3.2 Update `GET /entries/<date>` to merge computed recurring instances with stored entries
- [x] 3.3 Update `GET /entries/range` (WhatsApp digest) to include recurring instances across the date range

## 4. Backend — Entry Edit/Delete Scope

- [x] 4.1 Update entry creation (`POST /entries`) to accept optional `recurrence` payload and delegate to recurrence creation
- [x] 4.2 Implement "edit this occurrence" logic: add date to `excluded_dates`, create exception entry with `is_exception=1`
- [x] 4.3 Implement "edit all future" logic: set old rule's `until_date` to D-1, create new rule from D with updated values

## 5. Frontend — Recurrence Picker Component

- [x] 5.1 Build collapsible "Repeat" section in the event creation form (toggle, frequency select, days-of-week checkboxes, until date picker)
- [x] 5.2 Show/hide day-of-week checkboxes based on selected frequency (only for Weekly)
- [x] 5.3 Wire creation form submit to call `POST /recurrences` when repeat is enabled, `POST /entries` otherwise

## 6. Frontend — Recurring Instance Display

- [x] 6.1 Add repeat icon (↻) to event entry cards that have a `recurrence_id` in the day view
- [x] 6.2 Update calendar month grid dot logic to also mark days with recurring instances

## 7. Frontend — Edit/Delete Scope Modals

- [x] 7.1 Build scope modal component with two options: "This event" / "This and all future events"
- [x] 7.2 Show scope modal when user clicks edit on a recurring event instance; skip modal for standalone entries
- [x] 7.3 Wire "Edit this event" choice to create exception entry flow
- [x] 7.4 Wire "Edit this and all future" choice to `PUT /recurrences/<id>` split flow
- [x] 7.5 Show scope modal when user clicks delete on a recurring event instance; skip modal for standalone entries
- [x] 7.6 Wire "Delete this event" choice to `POST /recurrences/<id>/exceptions` flow
- [x] 7.7 Wire "Delete this and all future" choice to `DELETE /recurrences/<id>` flow

## 8. Frontend — Recurrence in Edit Form

- [x] 8.1 Pre-fill recurrence picker fields when editing a recurring event (all future scope)
- [x] 8.2 Disable recurrence picker when editing a single occurrence (exception scope — it's a standalone override)
