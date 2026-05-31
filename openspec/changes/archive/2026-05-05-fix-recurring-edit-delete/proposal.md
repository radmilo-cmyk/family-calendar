## Why

Recurring event edit and delete buttons do not work. The root cause is an HTML escaping bug: the `onclick` attributes pass string values (content, author) through Jinja2's `|tojson` filter, which wraps them in double quotes. Since the `onclick` attribute itself is delimited by double quotes, the browser treats the first `"` in the value as the end of the attribute — making the buttons completely non-functional.

## What Changes

- Replace inline `onclick` parameter passing with `data-*` attributes on the button elements
- JavaScript reads data attributes from the event target instead of receiving values as function arguments
- No backend changes required — the server-side routes already work correctly

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `entry-edit`: Fix the recurring event edit and delete scope modal — buttons must actually trigger the modal

## Impact

- Only `app/templates/day.html` changes
- No backend, CSS, or spec-level behavior changes beyond what is already specified
