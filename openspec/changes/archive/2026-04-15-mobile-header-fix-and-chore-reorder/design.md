## Context

Flask/Jinja2 app. Header in `app/templates/base.html`, styles in `app/static/style.css`. Default chores managed via `app/default_chores.py` and `app/templates/settings.html`. Daily view in `app/templates/day.html`.

Current header: `display: flex; justify-content: space-between; flex-wrap: wrap`. On narrow mobile screens the site-title and nav wrap to separate lines — when nav wraps to its own row, space-between collapses and all three nav links appear bunched together (no left-anchor element to push against).

Default chores have no `sort_order` column. Fetch order is undefined (insertion order from DB). Settings page renders a plain list with no reorder UI.

## Goals / Non-Goals

**Goals:**
- Header always shows title left, nav right on all screen sizes
- Default chores settings page has drag-to-reorder
- Daily view renders chores in the user-defined sort order

**Non-Goals:**
- Redesigning the header for mobile (hamburger menu, collapse)
- Per-user chore ordering (order is shared / family-level)
- Reordering regular (non-default) chores

## Decisions

**Header fix — remove flex-wrap, shrink title font on mobile**
Add a `@media (max-width: 480px)` block that sets `flex-wrap: nowrap` and reduces `.site-title` font-size so both elements fit on one row. Alternative (hide site-title on mobile) was rejected — user wants parity with desktop, not a stripped-down view.

**Drag-to-reorder — HTML5 drag-and-drop, no library**
Use native `draggable` attribute + JS drag events on the chore list items. Sends a PATCH request with the new ordered list of IDs to a `/settings/default-chores/reorder` endpoint. No external dependency needed for a simple list. Alternative (SortableJS) would add a CDN dependency for a feature that native events handle fine.

**sort_order column — integer, re-indexed on every reorder**
Add `sort_order INTEGER DEFAULT 0` to `default_chores` table. On reorder, update all rows with sequential values (0, 1, 2…). Simple and collision-free. Alternative (fractional indexing) is overkill for a list of ~10 chores.

**Daily view fetch — ORDER BY sort_order ASC**
Change the SQL/ORM query that loads default chores for the day view to sort by `sort_order`. No UI change needed in day.html — just the query.

## Risks / Trade-offs

- `flex-wrap: nowrap` on very small screens (< 320px) could clip the logout text → Mitigation: hide "Log out (username)" label text, keep just "Log out" or truncate with CSS ellipsis if needed
- Drag-and-drop is touch-unfriendly on mobile → Mitigation: acceptable for settings page (not a primary mobile flow); can be improved later
- Re-indexing all sort_order values on each reorder is a full table update → acceptable for ≤ 20 chores

## Migration Plan

1. Add `sort_order` column via new migration file in `migrations/`
2. Backfill existing rows with sequential values based on current rowid
3. Deploy: migration runs on startup (app already applies migrations automatically)
4. Rollback: remove column (non-breaking, query falls back to insertion order)
