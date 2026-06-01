# calendar-view Specification

## Purpose
TBD - created by archiving change family-calendar-app. Update Purpose after archive.
## Requirements
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

### Requirement: Day view displays event entries sorted by type then time
The day view SHALL display event-type entries in the following order: all-day events first (those with `time_start = NULL`), then timed events in ascending order of `time_start`. All-day events SHALL be visually marked with an "All day" badge. Timed events SHALL display their start time (and end time if present) as a label.

#### Scenario: All-day events appear before timed events
- **WHEN** a day has both all-day and timed event entries
- **THEN** all-day events SHALL render at the top of the events section
- **AND** timed events SHALL render below, ordered by `time_start` ascending

#### Scenario: All-day event badge shown
- **WHEN** an event entry has `time_start = NULL`
- **THEN** the entry card SHALL display an "All day" badge

#### Scenario: Timed event displays time label
- **WHEN** an event entry has `time_start` set
- **THEN** the entry card SHALL display the time in HH:MM format (e.g. "14:00 – 15:00" or "14:00" if no end time)

#### Scenario: Multiple timed events sorted correctly
- **WHEN** a day has timed events at 14:00, 09:00, and 11:30
- **THEN** they SHALL render in order: 09:00, 11:30, 14:00

### Requirement: Recurring event instances are visually distinguished in day view
Recurring event entries in the day view SHALL display a repeat icon (e.g. ↻) to indicate they are part of a series.

#### Scenario: Recurring instance shows repeat icon
- **WHEN** the day view displays a recurring event instance
- **THEN** the entry card SHALL show a small repeat icon alongside the event content

#### Scenario: Standalone event shows no repeat icon
- **WHEN** the day view displays a standalone (non-recurring) event
- **THEN** the entry card SHALL NOT show a repeat icon

### Requirement: Calendar is usable on mobile browser
The system SHALL render the calendar grid in a way that is legible and tappable on a small screen (minimum 320px wide).

#### Scenario: Mobile display
- **WHEN** the calendar is viewed on a mobile screen
- **THEN** all day cells are visible without horizontal scrolling and are large enough to tap

