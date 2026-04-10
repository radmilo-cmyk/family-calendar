## 1. Backend — Service Layer

- [x] 1.1 Add `update_entry(db, entry_id, content, author, entry_type)` to `app/entries.py`

## 2. Backend — Route

- [x] 2.1 Add `POST /entries/<int:entry_id>/edit` route in `app/main.py`
- [x] 2.2 Route reads form fields, calls `update_entry()`, redirects to `/day/<date>`

## 3. Frontend — HTML

- [x] 3.1 Add pencil SVG icon definition to `day.html` (beside existing `icon_delete`)
- [x] 3.2 Add edit button (`btn-edit`) inside `entry_list` macro, left of delete button
- [x] 3.3 Add hidden inline edit form (`edit-form`) inside each `<li>`, pre-filled with `entry.content`, `entry.author`, `entry.type`
- [x] 3.4 Edit form includes `content` textarea, `author` input, `entry_type` select, Save + Cancel buttons
- [x] 3.5 Edit form POSTs to `/entries/{{ entry.id }}/edit`

## 4. Frontend — CSS

- [x] 4.1 Add `.btn-edit` style (same size as `.btn-delete`, teal on hover instead of red)
- [x] 4.2 Add `.edit-form` style (hidden by default, padded card below entry row)
- [x] 4.3 Add `.entry-item.editing .edit-form` to show form when `.editing` class is on `<li>`
- [x] 4.4 Add entry action buttons wrapper `.entry-actions` so edit + delete sit side-by-side

## 5. Frontend — JavaScript

- [x] 5.1 Add JS in `day.html` to toggle `.editing` class on edit button click
- [x] 5.2 Close any other open edit forms before opening a new one (one-at-a-time rule)
- [x] 5.3 Add Escape key listener to close the active edit form

## 6. Verification

- [x] 6.1 Edit an event — confirm updated content appears after save
- [x] 6.2 Edit author name — confirm it updates
- [x] 6.3 Change entry type (e.g. event → chore) — confirm it moves to correct section
- [x] 6.4 Cancel edit — confirm no changes saved
- [x] 6.5 Open two edit forms rapidly — confirm only one is open at a time
