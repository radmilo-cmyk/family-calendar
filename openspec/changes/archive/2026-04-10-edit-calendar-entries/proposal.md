## Why

Calendar entries can only be deleted — any mistake or update requires deleting and re-adding from scratch. Editing in place is a basic CRUD capability that removes friction for the whole family.

## What Changes

- Add an edit button (pencil icon) next to each entry's delete button
- Inline edit form expands below the entry on click — no page navigation needed
- Form pre-fills with current `content`, `author`, and `entry_type`
- Save commits the change via POST; Cancel collapses the form
- New backend route: `POST /entries/<id>/edit`
- New backend function: `update_entry()` in `entries.py`

## Capabilities

### New Capabilities

- `entry-edit`: Inline editing of existing calendar entries (content, author, type) from the day view

### Modified Capabilities

<!-- none — existing delete/add flows are unchanged -->

## Impact

- **Templates**: `app/templates/day.html` — add edit button + inline form to `entry_list` macro
- **CSS**: `app/static/style.css` — add styles for edit button, inline edit form, and animated expand/collapse
- **Routes**: `app/main.py` — new `POST /entries/<id>/edit` route
- **Service**: `app/entries.py` — new `update_entry()` function
- **No DB schema changes** — existing `Entry` model covers all editable fields
