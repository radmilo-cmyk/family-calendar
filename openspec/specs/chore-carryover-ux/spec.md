# chore-carryover-ux Specification

## Purpose
Defines how carried-over chores are visually distinguished in the day view from freshly-added chores.

## Requirements

### Requirement: Visual carryover badge on rolled-over chores
The day view SHALL display a badge or label next to any chore Entry where `carried_over=True`, showing the `original_date` in a human-readable format (e.g. "↩ from Apr 12"). Fresh chores (carried_over=False) SHALL show no such indicator.

#### Scenario: Carried-over chore shows badge
- **WHEN** the day view renders a chore Entry with `carried_over=True`
- **THEN** a badge or label (e.g. "↩ from Apr 12") appears alongside the chore content, showing the `original_date`

#### Scenario: Fresh chore shows no badge
- **WHEN** the day view renders a chore Entry with `carried_over=False`
- **THEN** no carryover indicator is shown — the chore looks identical to its current appearance

#### Scenario: Carried-over chore can still be completed
- **WHEN** a user checks a carried-over chore
- **THEN** it toggles done state normally — the badge remains visible but the row is styled as completed (same as any done chore)
