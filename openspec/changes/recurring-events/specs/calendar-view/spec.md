## MODIFIED Requirements

### Requirement: Monthly calendar grid is displayed
The system SHALL display a monthly calendar grid showing all days of the current month. Days that have at least one entry (including recurring event instances) SHALL be visually marked.

#### Scenario: View current month
- **WHEN** an authenticated user visits `/`
- **THEN** the system displays a calendar grid for the current month in the Europe/Amsterdam timezone

#### Scenario: Day with entries is marked
- **WHEN** a day has one or more entries (standalone or recurring instances)
- **THEN** that day's cell in the grid shows a visual indicator (e.g. a dot or highlight)

#### Scenario: Day with only recurring instance is marked
- **WHEN** a day has no standalone entries but has one or more recurring event instances
- **THEN** that day's cell in the grid SHALL show the visual indicator

#### Scenario: Day with no entries
- **WHEN** a day has no entries and no recurring instances apply
- **THEN** that day's cell is displayed without any indicator

## ADDED Requirements

### Requirement: Recurring event instances are visually distinguished in day view
Recurring event entries in the day view SHALL display a repeat icon (e.g. ↻) to indicate they are part of a series.

#### Scenario: Recurring instance shows repeat icon
- **WHEN** the day view displays a recurring event instance
- **THEN** the entry card SHALL show a small repeat icon alongside the event content

#### Scenario: Standalone event shows no repeat icon
- **WHEN** the day view displays a standalone (non-recurring) event
- **THEN** the entry card SHALL NOT show a repeat icon
