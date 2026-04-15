## Context

The app is FastAPI + SQLAlchemy + Jinja2 templates + vanilla JS. No Alembic — tables are created via `Base.metadata.create_all()` on startup. DB is SQLite locally and PostgreSQL (Supabase) in production. Auth uses a session cookie; any logged-in user can act.

Current chore flow: user types a chore on the day view → it's saved as an `Entry(type="chore")` row → displayed in a `<ul>` list. No completion state. No recurring defaults.

## Goals / Non-Goals

**Goals:**
- Add `done` / `done_by` state to chore entries, toggleable by any user
- Render chores as an interactive checklist on the day view
- Provide a `DefaultChore` table for globally configured recurring chores
- Show default chores on every day view without pre-populating the DB with unchecked rows
- Provide a `/settings` page to manage the default chores list

**Non-Goals:**
- Per-user default chore assignments
- Chore history or audit log beyond `done_by`
- Due dates or reminders for chores
- Modifying the existing event or message entry types

## Decisions

### 1. Chore completion stored on Entry model

Add `done` (Boolean, default=False) and `done_by` (String, nullable) columns to the existing `Entry` table.

**Why not a separate `chore_completions` table?** The `Entry` model is already per-day-per-type. Adding two columns is simpler and avoids a join on every day view load. The `done_by` field is enough to show who completed it.

**Migration strategy:** `create_all()` only creates new tables/columns if they don't exist in SQLite. PostgreSQL requires `ALTER TABLE` — add an Alembic-style raw migration script (since Alembic is not set up, a one-time SQL script run on Supabase dashboard is acceptable).

### 2. Default chores rendered as virtual items (no DB pre-population)

Default chores are stored in a new `DefaultChore(id, content, position)` table. On `GET /day/<date>`, the route fetches both real chores for that date and the full default chores list. The template merges them: defaults not yet represented in real chores appear as "virtual" unchecked rows; real chores appear as normal toggleable rows.

**Why not auto-insert defaults on GET?** That introduces a DB write on every GET for a new day — unexpected side effect. Virtual rendering avoids it.

**Matching logic:** A default chore is "already present" if a real Entry for that date has `content` matching the default's content (case-insensitive). If matched, the real entry is shown (with its actual done state). If not matched, the virtual row is shown.

**Checking a virtual default chore** → form POST to a new endpoint `POST /day/<date>/chores/complete-default` that creates an Entry for that chore + sets `done=True`, `done_by=current_user` in one step.

**Unchecking a real chore** (whether default-sourced or user-added) → `POST /entries/<id>/toggle`.

### 3. Settings page at `/settings`

A new page linked from the calendar header (gear icon, top right). Shows the default chores list with add/remove controls. This keeps settings separate from the day view, avoiding clutter.

**Why not a modal or sidebar on the calendar?** The calendar view is already compact. A dedicated page is simpler to implement without a JS-heavy modal, consistent with the existing multi-page approach.

### 4. Toggle is a POST, not AJAX

Consistent with the rest of the app (all mutations are form POSTs with redirect). No JS needed for toggling — the checkbox submits a hidden form. Keeps the codebase uniform.

## Risks / Trade-offs

- **Matching by content string is fragile** → if a default chore's text is edited, old days lose the match. Mitigation: content match is only for display merging, not data integrity. Real entries always show correctly regardless.
- **GET /day reads DefaultChore table on every request** → negligible for a family-scale app with a handful of defaults.
- **PostgreSQL migration is manual** → document the two `ALTER TABLE` statements to run in Supabase SQL editor before deploying.

## Migration Plan

1. Run on Supabase SQL editor before deploy:
   ```sql
   ALTER TABLE entries ADD COLUMN IF NOT EXISTS done BOOLEAN DEFAULT FALSE;
   ALTER TABLE entries ADD COLUMN IF NOT EXISTS done_by VARCHAR;
   CREATE TABLE IF NOT EXISTS default_chores (
     id SERIAL PRIMARY KEY,
     content VARCHAR NOT NULL,
     position INTEGER DEFAULT 0
   );
   ```
2. Deploy new code — `create_all()` handles SQLite automatically
3. Rollback: columns are additive; removing them is a separate SQL step if needed

## Open Questions

- Should checked-off default chores be visually moved to the bottom of the list, or stay in position? (Recommendation: stay in position, like a standard checklist)
- Should there be a max number of default chores? (Recommendation: soft cap at 10, enforced in UI only)

---

## UX Solutions

### Chore Checklist (Day View)

Chores section replaces `<ul>` with a checklist. Each row has:

```
[ ] Vacuum living room           — Radmilo    [edit] [x]
[✓] Do laundry          done by Maja          [edit] [x]
```

- **Checkbox on the left** — large tap target (44×44px), uses native `<input type="checkbox">` styled with CSS
- **Checked state** — text gets a strikethrough + muted color + "done by [name]" label appears
- **Virtual defaults** (not yet done) — same appearance as unchecked, but submit to the `complete-default` endpoint instead of toggle
- **Interaction**: checkbox submits its hidden sibling `<form>` via JS `form.submit()` on change — single click, no button needed
- **Undo-friendly**: unchecking works identically, so accidental checks are easily reversed

**Visual language** (matching existing design system):
- Checkbox: `2px` border, `border-radius: 4px`, accent color fill when checked (use existing `--accent` CSS variable)
- Strikethrough text: `text-decoration: line-through; opacity: 0.5`
- "done by" badge: same `entry-author` style already in use
- No animation needed — keep it as fast as the existing delete/edit flow

### Default Chores Settings (Calendar View Header)

**Entry point**: small gear icon (`⚙`) in the top-right of the calendar header, next to the user name / logout link. Links to `/settings`.

```
[← April 2026]  [Family Calendar]  [Maja ⚙ logout]
```

**Settings page (`/settings`)**:
- Minimal page, same `base.html` wrapper
- Single card: "Default Daily Chores"
- Lists current defaults with a remove button [×] per row
- Inline add form at the bottom: text input + "Add" button
- Order controlled by `position` field; drag-to-reorder is out of scope (manual order via add sequence)

```
Default Daily Chores
────────────────────
  Vacuum living room    [×]
  Do laundry            [×]
  Take out trash        [×]

  [_________________________] [Add]
```

- Style: same `.entry-section` card used on day view
- Remove: form POST to `DELETE /settings/default-chores/<id>` (via POST with `_method` override or direct POST)
- Add: form POST to `POST /settings/default-chores`
- Success: redirect back to `/settings` (same pattern as entry add/delete)
