## Context

Flask + Jinja2 app. Day view renders entries as a list with a delete button per item. No JS framework — vanilla JS only. Design system uses warm teal tokens, Caveat/Quicksand fonts, 12px radius cards.

## Goals / Non-Goals

**Goals:**
- Inline edit (no page navigation) matching existing card/button design language
- Edit `content`, `author`, and `entry_type` fields
- Keyboard-accessible (Escape to cancel, Enter to submit)

**Non-Goals:**
- Changing the entry `date` (move-to-day is out of scope)
- Optimistic UI / AJAX — full page reload on save is fine
- Edit history / audit trail

## Decisions

**1. Inline expand vs. modal**
Chose inline expand (hidden form slides open below entry row) over a modal.
- Stays in context of the day's list
- No overlay/focus-trap complexity
- Consistent with the existing add-entry form pattern at the bottom of the page

**2. HTTP method**
`POST /entries/<id>/edit` — standard HTML form POST, no JS fetch required.
Server redirects back to `/day/<date>` on success.

**3. State toggle via CSS class + tiny JS**
One `<script>` block handles show/hide of all inline forms on the page.
No new libraries. Toggle `.editing` class on the `<li>`.

**4. Pencil icon placement**
Edit button sits left of the existing delete (X) button.
Same size (16×16), same ghost-button style — secondary teal on hover, not destructive red.

## Risks / Trade-offs

- [Multi-click spam] User clicks edit on multiple entries → multiple forms open simultaneously.
  → Mitigation: JS closes any open form before opening a new one.

- [Form pre-fill] Jinja renders pre-filled values server-side — no stale-data risk.

## Migration Plan

1. Add `update_entry()` to `entries.py`
2. Add route in `main.py`
3. Update `day.html` macro — add edit button + hidden form inside `<li>`
4. Add CSS for `.btn-edit`, `.edit-form`, `.editing` state
5. Deploy — no DB migration needed
