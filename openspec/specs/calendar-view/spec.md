# calendar-view Specification

## Purpose
TBD - created by archiving change family-calendar-app. Update Purpose after archive.
## Requirements
### Requirement: Monthly calendar grid is displayed
The system SHALL display a monthly calendar grid showing all days of the current month. Days that have at least one entry SHALL be visually marked.

#### Scenario: View current month
- **WHEN** an authenticated user visits `/`
- **THEN** the system displays a calendar grid for the current month in the Europe/Amsterdam timezone

#### Scenario: Day with entries is marked
- **WHEN** a day has one or more entries
- **THEN** that day's cell in the grid shows a visual indicator (e.g. a dot or highlight)

#### Scenario: Day with no entries
- **WHEN** a day has no entries
- **THEN** that day's cell is displayed without any indicator

### Requirement: User can navigate between months
The system SHALL provide previous and next controls to navigate to adjacent months.

#### Scenario: Navigate to next month
- **WHEN** the user clicks the next month control
- **THEN** the calendar updates to display the following month

#### Scenario: Navigate to previous month
- **WHEN** the user clicks the previous month control
- **THEN** the calendar updates to display the preceding month

### Requirement: Clicking a day opens the day view
The system SHALL make each day cell a link to the day detail view for that date.

#### Scenario: Click a day
- **WHEN** the user clicks on a day cell
- **THEN** the system navigates to `/day/YYYY-MM-DD` for that date

### Requirement: Calendar is usable on mobile browser
The system SHALL render the calendar grid in a way that is legible and tappable on a small screen (minimum 320px wide).

#### Scenario: Mobile display
- **WHEN** the calendar is viewed on a mobile screen
- **THEN** all day cells are visible without horizontal scrolling and are large enough to tap

