# calendar-ux Specification

## Purpose
TBD - created by archiving change ui-ux-improvement. Update Purpose after archive.
## Requirements
### Requirement: Calendar cells are taller and touch-friendly
Each calendar day cell SHALL be at least 56px tall (up from 48px) to meet the 44px minimum touch target requirement with comfortable padding.

#### Scenario: Day tap target on mobile
- **WHEN** a user taps a calendar day on a 375px viewport
- **THEN** the tap target SHALL be at least 44×44px

### Requirement: Today's date is visually highlighted
The current day cell SHALL render a teal ring (outline or border) and bold day number so it is immediately identifiable without relying solely on color.

#### Scenario: Today highlight visible
- **WHEN** the calendar displays the current month
- **THEN** today's cell SHALL have a distinct ring in `--color-primary` and the day number SHALL be bold

### Requirement: Entry indicator uses a dot, not a background fill
Days with entries SHALL show a small colored dot (≤8px) below the day number instead of filling the entire cell background.

#### Scenario: Entry dot renders
- **WHEN** a day has at least one entry
- **THEN** a teal dot SHALL appear below the day number

#### Scenario: Dot does not obscure day number
- **WHEN** a day has entries and the cell is at minimum size
- **THEN** the day number and dot are both fully visible with no overlap

### Requirement: Day cells have hover feedback
Each day cell link SHALL show a visible hover state (background color change + cursor-pointer) to indicate it is clickable.

#### Scenario: Hover state on desktop
- **WHEN** a user hovers over a day cell
- **THEN** the cell background transitions to a light teal tint within 150ms and `cursor-pointer` is applied

