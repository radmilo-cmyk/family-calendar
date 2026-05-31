## Context

The recurring event buttons in `day.html` call `openRecurringModal(...)` with string values (content, author) passed directly as `onclick` parameters using `|tojson`. In HTML, `onclick="..."` uses double quotes as delimiters. `|tojson` also wraps strings in double quotes. The result is broken HTML that the browser cannot parse.

Example of the broken output:
```html
onclick="openRecurringModal('edit', 5, '2026-05-04', "recurring-5", "Football", "Radmilo", '', '')"
```
The browser treats `onclick` as ending at the first `"` before `recurring-5`.

## Goals / Non-Goals

**Goals:**
- Make recurring event edit and delete buttons functional
- Keep the fix minimal and contained to `day.html`

**Non-Goals:**
- Changing the scope modal UX or the backend routes
- Refactoring unrelated JS

## Decisions

### Use data-* attributes instead of inline onclick parameters

**Decision**: Store all values needed by the modal on the button element as `data-*` attributes. A single delegated JS event listener reads them on click.

**Why**: `data-*` attributes are HTML-attribute-safe — values are HTML-escaped by Jinja2's `{{ value|e }}` filter, avoiding the double-quote collision entirely. It also makes the template cleaner and the JS easier to maintain.

**Implementation**:

Button element (edit):
```html
<button type="button" class="btn-edit"
  data-action="edit"
  data-rule-id="{{ entry.recurrence_id }}"
  data-date="{{ day.isoformat() }}"
  data-content="{{ entry.content|e }}"
  data-author="{{ entry.author|e }}"
  data-ts="{{ entry.time_start.strftime('%H:%M') if entry.time_start else '' }}"
  data-te="{{ entry.time_end.strftime('%H:%M') if entry.time_end else '' }}"
  onclick="openRecurringModal(this)">
```

JS function signature changes to:
```javascript
function openRecurringModal(btn) {
  var action  = btn.dataset.action;
  var ruleId  = btn.dataset.ruleId;
  var dateStr = btn.dataset.date;
  var content = btn.dataset.content;
  var author  = btn.dataset.author;
  var ts      = btn.dataset.ts;
  var te      = btn.dataset.te;
  ...
}
```

## Risks / Trade-offs

- Minimal risk — purely a frontend template fix with no logic changes
- `|e` (HTML escape) is the correct filter for attribute values in Jinja2; content like `<` or `&` in event titles will render correctly
