## MODIFIED Requirements

### Requirement: Monthly calendar grid is displayed
The system SHALL display a monthly calendar grid showing all days of the current month. Days that have at least one entry (including recurring event instances) SHALL be visually marked. Below the grid, the system SHALL render a read-only agenda list of upcoming events (see `home-agenda-list` spec for full agenda requirements).

#### Scenario: View current month
- **WHEN** an authenticated user visits `/`
- **THEN** the system displays a calendar grid for the current month in the Europe/Amsterdam timezone
- **AND** a read-only agenda list of upcoming events is rendered below the grid

#### Scenario: Day with entries is marked
- **WHEN** a day has one or more entries (standalone or recurring instances)
- **THEN** that day's cell in the grid shows a visual indicator (e.g. a dot or highlight)

#### Scenario: Day with only recurring instance is marked
- **WHEN** a day has no standalone entries but has one or more recurring event instances
- **THEN** that day's cell in the grid SHALL show the visual indicator

#### Scenario: Day with no entries
- **WHEN** a day has no entries and no recurring instances apply
- **THEN** that day's cell is displayed without any indicator
