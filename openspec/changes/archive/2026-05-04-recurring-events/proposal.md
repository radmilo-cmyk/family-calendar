## Why

Family events often repeat on a schedule (weekly sports practice, recurring dinners) but today every occurrence must be added manually. Recurring events reduce friction and make the calendar actually reflect real family life.

## What Changes

- Events can be marked as recurring when created or edited
- Recurrence options: daily, weekly (with day-of-week selection), or monthly
- Each recurrence has an end date (`until`)
- Recurring event instances appear automatically across the calendar
- Editing a recurring event offers: edit this occurrence only, or edit all future occurrences
- Deleting a recurring event offers: delete this occurrence only, or delete all future occurrences

## Capabilities

### New Capabilities
- `event-recurrence`: Core recurrence model — storing recurrence rules (frequency, days of week, until date), generating instances on-the-fly or via expansion, and managing the lifecycle of a recurrence series (create, edit single vs. all-future, delete single vs. all-future)

### Modified Capabilities
- `entry-management`: Entry storage gains recurrence fields (`recurrence_id`, `recurrence_rule`); creation, deletion, and querying must account for recurring instances
- `entry-edit`: Add recurrence picker to the event creation and edit forms; expose edit-scope choice (this / all future) when editing a recurring event
- `calendar-view`: Month grid and day view must surface recurring event instances correctly (dot indicators, entry listing)

## Impact

- **Database**: New `recurrences` table (rule storage); entries gain nullable `recurrence_id` FK and `is_exception` flag
- **Backend API**: New endpoints for recurrence CRUD; entry creation/deletion/edit endpoints updated to handle recurrence scope
- **Frontend**: Recurrence picker component; edit/delete scope modal; recurring entries visually distinguished (e.g. repeat icon)
- **No breaking changes** to existing non-recurring events or other entry types
