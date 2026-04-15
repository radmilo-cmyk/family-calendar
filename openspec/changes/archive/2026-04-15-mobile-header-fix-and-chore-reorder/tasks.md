## 1. Database Migration

- [x] 1.1 Create migration file in `migrations/` to add `sort_order INTEGER DEFAULT 0` column to `default_chores` table
- [x] 1.2 Add backfill SQL in the migration to set sequential `sort_order` values for existing rows based on `rowid`

## 2. Mobile Header Fix

- [x] 2.1 Add `@media (max-width: 480px)` block in `app/static/style.css` that sets `flex-wrap: nowrap` on `header` and reduces `.site-title` font-size so title and nav fit on one row

## 3. Chore Ordering Backend

- [x] 3.1 Update `app/default_chores.py` — when adding a new default chore, set `sort_order` to `MAX(sort_order) + 1`
- [x] 3.2 Update `app/default_chores.py` — all fetch queries for default chores to use `ORDER BY sort_order ASC`
- [x] 3.3 Add `POST /settings/default-chores/reorder` route in `app/default_chores.py` that accepts a JSON array of chore IDs and updates each row's `sort_order` sequentially
- [x] 3.4 Register the reorder route in `app/main.py` (or wherever blueprints are wired)

## 4. Chore Ordering Frontend

- [x] 4.1 In `app/templates/settings.html` — add `draggable="true"` to each default chore list item and a drag handle icon
- [x] 4.2 Add inline JS in `settings.html` — drag event listeners (`dragstart`, `dragover`, `drop`) that reorder the DOM list
- [x] 4.3 On drop, JS sends `fetch` PATCH/POST to `/settings/default-chores/reorder` with the new ordered array of chore IDs

## 5. Day View Integration

- [x] 5.1 Verify default chore fetch in `app/entries.py` (or wherever day view loads chores) uses `ORDER BY sort_order ASC` — update if not

## 6. Verification

- [ ] 6.1 Test mobile header on a narrow viewport (e.g. 375px): title left, nav right on same row
- [ ] 6.2 Test drag reorder on settings page: drag a chore, reload, confirm order persists
- [ ] 6.3 Test day view: chores appear in the order set on settings page

