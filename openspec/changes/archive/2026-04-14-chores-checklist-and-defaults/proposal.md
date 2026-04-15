## Why

Chores are currently a plain list with no way to track completion — family members can't see what's already been done by whom. There's also no way to define recurring daily tasks (dishes, trash, etc.), so the same chores must be added manually every day.

## What Changes

- Chores section on the day view becomes an interactive checklist — each chore can be checked as done or unchecked if it was marked by mistake
- A new "Default Chores" feature lets the family define a global list of chores that automatically appear on every day's view
- A dedicated settings section (accessible from the main calendar view) lets any user manage the default chores list (add, remove)
- Default chores appear as unchecked items each day; user-added chores continue to work as before but also gain the checkbox

## Capabilities

### New Capabilities
- `chore-completion`: Chores have a done/undone state stored in the database. Any user can toggle a chore between done and undone. The toggle is reflected immediately and shows who completed it.
- `default-chores`: A global list of default chore templates. Each day view auto-populates the chores section with these defaults (as unchecked items). Users can manage this list from a settings panel on the calendar.

### Modified Capabilities
- `entry-management`: Entry model gains a `done` boolean field (default false) and `done_by` string field to record who completed it. Only relevant for chore-type entries.
- `day-view`: Chores section renders as a checklist instead of a plain list. Each item has a checkbox that POSTs to a toggle endpoint. Default chores are injected at render time from the defaults list.

## Impact

- **Database**: `entries` table gains `done` (Boolean) and `done_by` (String, nullable) columns — requires a migration
- **New table**: `default_chores` table to store the global default chore list
- **New routes**: `POST /entries/<id>/toggle` for completion toggle; `GET/POST /settings/default-chores` for managing defaults
- **Templates**: `day.html` chores section updated to render checkboxes; new settings UI component added to `calendar.html` or as a separate page
- **No breaking changes** to events or messages
