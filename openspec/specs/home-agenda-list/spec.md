# home-agenda-list Specification

## Purpose
Read-only agenda strip below the monthly calendar grid on the home page, showing all upcoming events (including recurring instances) paginated by date group.

## Requirements

### Requirement: Agenda list displays upcoming events below the calendar grid
The system SHALL render a read-only agenda list below the monthly calendar grid on the home page. The list SHALL show event-type entries (`type == "event"`), including virtual recurring instances. The agenda SHALL show all events from today onward (up to 1 year ahead) regardless of which month is currently viewed in the calendar grid. The agenda section SHALL be hidden entirely if there are no upcoming events.

#### Scenario: Current month with upcoming events
- **WHEN** an authenticated user visits the home page for the current month
- **AND** there are event entries on dates from today onward
- **THEN** the agenda list SHALL appear below the calendar grid
- **AND** each date with events SHALL appear as a row with the date on the left and event titles on the right

#### Scenario: Recurring event appears in agenda
- **WHEN** a recurring rule has an occurrence on a future date
- **THEN** that occurrence SHALL appear in the agenda list on its date

#### Scenario: Edited recurring occurrence shown correctly
- **WHEN** a single occurrence of a recurring event has been edited
- **THEN** the agenda SHALL show the edited version (not the original rule content) for that date

#### Scenario: Past month view still shows upcoming agenda
- **WHEN** the user navigates to a past month
- **THEN** the agenda list SHALL still display upcoming events from today onward

#### Scenario: No upcoming events
- **WHEN** there are no event entries on today or any future date
- **THEN** the agenda section SHALL NOT be rendered

### Requirement: Agenda rows are grouped by date, sorted ascending
The agenda list SHALL group events under their date. Multiple events on the same date SHALL appear stacked under one date label. Dates SHALL be displayed in ascending order (earliest first).

#### Scenario: Multiple events on same date
- **WHEN** two or more events exist on the same qualifying date
- **THEN** they SHALL appear under a single date label, stacked vertically

#### Scenario: Events on multiple dates
- **WHEN** events exist on three different qualifying dates
- **THEN** the date with the earliest date SHALL appear first in the list

### Requirement: Agenda is paginated by date group
The agenda list SHALL show up to 5 date groups per page. When more than 5 date groups exist, "Earlier" and "Later" navigation links SHALL be shown. Navigation links SHALL preserve the calendar grid's current `year` and `month` query params.

#### Scenario: More than 5 date groups
- **WHEN** there are events on more than 5 upcoming dates
- **THEN** the agenda SHALL show the first 5 date groups with a "Later" navigation link

#### Scenario: Navigate to next page
- **WHEN** the user clicks "Later"
- **THEN** the next 5 date groups are shown and an "Earlier" link appears

#### Scenario: First page has no Earlier link
- **WHEN** the user is on agenda page 0
- **THEN** the "Earlier" control SHALL be visually disabled (not a link)

### Requirement: Each event row shows content and time if applicable
Each event in the agenda list SHALL display its `content` (title). If the event has a `time_start`, it SHALL also display the time. If it also has a `time_end`, it SHALL display the range. All-day events (no `time_start`) SHALL show no time label.

#### Scenario: Timed event in agenda
- **WHEN** an event has `time_start = 10:00` and `time_end = 11:00`
- **THEN** the agenda row SHALL show "10:00 – 11:00" alongside the event title

#### Scenario: All-day event in agenda
- **WHEN** an event has `time_start = NULL`
- **THEN** the agenda row SHALL show only the event title with no time label

### Requirement: Clicking an agenda row navigates to the day view
Each date row in the agenda SHALL be a link. Clicking anywhere on the row SHALL navigate to `/day/YYYY-MM-DD` for that date. No inline editing or forms are present in the agenda list.

#### Scenario: Click agenda date row
- **WHEN** the user clicks on an agenda date row
- **THEN** the browser navigates to the day view for that date

#### Scenario: No edit controls in agenda
- **WHEN** the agenda list is displayed
- **THEN** there SHALL be no edit, delete, or add buttons anywhere in the agenda section

### Requirement: Agenda list matches the existing visual design system
The agenda section SHALL use the same CSS design tokens as the rest of the app: teal palette (`--color-primary`, `--color-border`, `--color-bg`), `Quicksand` font, `--radius: 12px` cards, and consistent spacing. It SHALL be legible on mobile (min 320px wide) without horizontal scrolling.

#### Scenario: Agenda on mobile
- **WHEN** the home page is viewed on a 320px wide screen
- **THEN** the agenda list SHALL be fully visible without horizontal scrolling

#### Scenario: Long event title
- **WHEN** an event title exceeds the available width
- **THEN** the title SHALL be truncated with an ellipsis rather than overflowing
