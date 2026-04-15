## 1. Database Model Changes

- [x] 1.1 Add `done` (Boolean, default=False) and `done_by` (String, nullable) columns to the `Entry` model in `app/models.py`
- [x] 1.2 Add new `DefaultChore` model to `app/models.py` with `id`, `content` (String), and `position` (Integer, default=0) columns
- [x] 1.3 Import `DefaultChore` in `app/main.py` lifespan so `create_all()` creates the new table on startup
- [x] 1.4 Document the two `ALTER TABLE` SQL statements needed for the Supabase PostgreSQL migration in a comment or a `migrations/` file

## 2. Data Access Layer

- [x] 2.1 Add `toggle_chore_done(db, entry_id, current_user)` function to `app/entries.py` — flips `done` and sets/clears `done_by`
- [x] 2.2 Add `complete_virtual_default(db, day, content, current_user)` function to `app/entries.py` — creates a chore Entry with `done=True` and `done_by=current_user`
- [x] 2.3 Add `get_all_default_chores(db)` function to a new `app/default_chores.py` module
- [x] 2.4 Add `create_default_chore(db, content)` function to `app/default_chores.py`
- [x] 2.5 Add `delete_default_chore(db, chore_id)` function to `app/default_chores.py`

## 3. New Routes

- [x] 3.1 Add `POST /entries/{entry_id}/toggle` route in `app/main.py` — calls `toggle_chore_done`, redirects back to the day view
- [x] 3.2 Add `POST /day/{date_str}/chores/complete-default` route in `app/main.py` — accepts `content` form field, calls `complete_virtual_default`, redirects back to day view
- [x] 3.3 Add `GET /settings` route in `app/main.py` — fetches all default chores, renders `settings.html`
- [x] 3.4 Add `POST /settings/default-chores` route in `app/main.py` — creates a new default chore, redirects to `/settings`
- [x] 3.5 Add `POST /settings/default-chores/{chore_id}/delete` route in `app/main.py` — deletes a default chore, redirects to `/settings`

## 4. Day View Template Update

- [x] 4.1 Update the day view route in `app/main.py` to also fetch `get_all_default_chores(db)` and pass to template as `default_chores`
- [x] 4.2 Compute `virtual_defaults` in the route: defaults whose content doesn't match any real chore entry for that day (case-insensitive), pass to template
- [x] 4.3 Rewrite the chores `entry_list` macro in `app/templates/day.html` to render checkboxes instead of plain list items
- [x] 4.4 Add checkbox toggle form for real chore entries (submits to `/entries/<id>/toggle`)
- [x] 4.5 Add virtual default chore rows at the top of the Chores section (unchecked, submit to `/day/<date>/chores/complete-default`)
- [x] 4.6 Show "done by [name]" label next to completed chore entries using the existing `entry-author` CSS class

## 5. Settings Page Template

- [x] 5.1 Create `app/templates/settings.html` extending `base.html` — shows default chores list with remove buttons and an add form
- [x] 5.2 Add gear icon link to `/settings` in `app/templates/base.html` (or `calendar.html`) in the header area next to user/logout

## 6. CSS Styling

- [x] 6.1 Add checkbox styles to `app/static/style.css`: large tap target, styled checked state using existing `--accent` color
- [x] 6.2 Add `.chore-done` class: `text-decoration: line-through; opacity: 0.5` for completed chore text
- [x] 6.3 Add `.chore-done-by` style for the "done by [name]" inline label (reuse `entry-author` or extend it)
- [x] 6.4 Style the settings page card to match the existing `.entry-section` visual language

## 7. JavaScript

- [x] 7.1 Add inline JS on `day.html` to submit the hidden toggle form when a checkbox `change` event fires (no page reload delay — form.submit() on change)
