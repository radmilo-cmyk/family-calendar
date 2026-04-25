## Why

Events in the family calendar currently have no concept of time — every entry is implicitly a full-day item. This makes it impossible to communicate *when* something happens during the day (e.g. "dentist at 14:00"), forcing users to embed time into the text content manually, which cannot be sorted, displayed, or reasoned about.

## What Changes

- **Event creation form** gains an optional time-range picker (start + end time) visible only when type = `event`. Leaving it empty defaults the entry to an all-day event.
- **Day view entry list** reorders to show: all-day events first (visually marked with an "all day" badge), then timed events sorted chronologically by `time_start`.
- **Database** gains two nullable `TIME` columns on `entries`: `time_start` and `time_end`. NULL = all-day.
- **Migration** sets `time_start = NULL` and `time_end = NULL` for all existing entries, classifying them as all-day retroactively.
- **Edit form** exposes the same time-range picker so users can promote an all-day event to a timed one (or clear the time to revert).

## Capabilities

### New Capabilities
- `event-time-slots`: Optional start/end time on event-type entries; all-day vs timed distinction; time picker UI in create and edit forms.

### Modified Capabilities
- `entry-management`: Entry model gains `time_start` / `time_end` nullable fields; create/edit APIs accept and store these; sort order logic changes for event-type entries.
- `entry-edit`: Edit form must expose and allow editing the time slot fields alongside existing content field.
- `calendar-view`: Day view rendering must apply the new sort order (all-day events pinned top, timed events below in chronological order) and display the all-day badge and time label.

## Impact

- **`app/models.py`** — add `time_start` (Time, nullable) and `time_end` (Time, nullable) columns to `Entry`
- **`app/entries.py`** — update create/edit/list endpoints; apply sort order in list query
- **`app/templates/day.html`** — time picker in create form (event type only), time picker in edit form, all-day badge, time label in entry display, reordered list render
- **`migrations/`** — new SQL migration to add columns (NULL default = backwards compatible)
- No dependency changes required
