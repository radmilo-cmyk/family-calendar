## Why

Mobile header layout breaks the visual hierarchy — all three elements (Calendar title, settings cog, logout) cluster to the right, losing the left-aligned title that desktop users expect. Default chores also have no ordering control, so the daily view shows chores in arbitrary database order rather than the user's preferred sequence.

## What Changes

- Fix mobile header so Calendar title aligns left, settings cog and logout button group to the right (matching desktop layout)
- Add drag-to-reorder UI on the Default Daily Chores settings page
- Persist chore order in the database
- Display chores in the daily view sorted by user-defined order

## Capabilities

### New Capabilities
- `chore-ordering`: Drag-to-reorder default chores on the settings page; order persists and drives daily view display sequence

### Modified Capabilities
- `default-chores`: Adds sort_order field and reorder interaction to existing default chores management
- `day-view`: Chores section renders in user-defined sort order instead of insertion order

## Impact

- `src/` — header component CSS/layout fix (mobile breakpoint)
- `src/` — DefaultChores settings page: drag-and-drop list
- Supabase `default_chores` table: new `sort_order` integer column
- Daily view chore fetch: ORDER BY sort_order
