## Context

Header currently has: logo (top-left, static image) + "Calendar" button (top-right). The button duplicates the logo's implicit home role. The logo needs an `<a>` wrapper pointing to `/` (or `index.html`) and a pointer cursor. The Calendar button is removed from all views that render it.

## Goals / Non-Goals

**Goals:**
- Logo navigates to calendar home on click
- Logo has hover affordance (cursor + subtle opacity or scale)
- Calendar button removed from every view

**Non-Goals:**
- Changing logo design or size
- Adding breadcrumbs or back-stack logic

## Decisions

**Wrap logo in anchor, not JS click handler** — native `<a>` gives free keyboard nav, right-click-open-in-tab, and accessibility for free.

**Hover style: opacity 0.8 on hover** — minimal, matches existing button hover patterns without adding new CSS variables.

## Risks / Trade-offs

- [Logo not obviously clickable] → Pointer cursor on hover is the standard affordance; no additional indicator needed at this scale
