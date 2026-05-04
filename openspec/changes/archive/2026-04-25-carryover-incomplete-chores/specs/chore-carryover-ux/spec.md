## ADDED Requirements

### Requirement: Visual carryover badge on rolled-over chores
The system SHALL render a visual indicator on any `Entry` where `carried_over=True` in the day view chores list. The indicator SHALL communicate that the chore was not done on a previous day and has been moved forward. The original date SHALL be displayed so users know how long the chore has been pending.

#### Scenario: Carried-over chore shows badge
- **WHEN** the day view renders a chore Entry with `carried_over=True`
- **THEN** a badge or label (e.g. "↩ from Apr 12") appears alongside the chore content, showing the `original_date`

#### Scenario: Fresh chore shows no badge
- **WHEN** the day view renders a chore Entry with `carried_over=False`
- **THEN** no carryover indicator is shown — the chore looks identical to its current appearance

#### Scenario: Carried-over chore can still be completed
- **WHEN** a user checks a carried-over chore
- **THEN** it toggles done state normally — the badge remains visible but the row is styled as completed (same as any done chore)
