## ADDED Requirements

### Requirement: Agenda list displays upcoming events below the calendar grid
The system SHALL render a read-only agenda list below the monthly calendar grid on the home page. The list SHALL show only event-type entries (`type == "event"`). When the viewed month is the current month, only events on today's date or later SHALL be shown. When the viewed month is a future month, all events in that month SHALL be shown. Past months SHALL show no agenda list. The agenda section SHALL be hidden entirely if there are no qualifying events.

#### Scenario: Current month with upcoming events
- **WHEN** an authenticated user visits the home page for the current month
- **AND** there are event entries on dates from today onward in that month
- **THEN** the agenda list SHALL appear below the calendar grid
- **AND** each date with events SHALL appear as a row with the date on the left and event titles on the right

#### Scenario: Current month with no upcoming events
- **WHEN** an authenticated user views the current month
- **AND** all event entries are in the past (before today)
- **THEN** the agenda section SHALL NOT be rendered

#### Scenario: Future month view
- **WHEN** the user navigates to a future month
- **AND** that month has event entries
- **THEN** all event entries in that month SHALL appear in the agenda list

#### Scenario: Past month view
- **WHEN** the user navigates to a past month
- **THEN** the agenda section SHALL NOT be rendered

#### Scenario: Empty month
- **WHEN** the viewed month has no event entries qualifying for display
- **THEN** the agenda section SHALL NOT be rendered

### Requirement: Agenda rows are grouped by date, sorted ascending
The agenda list SHALL group events under their date. Multiple events on the same date SHALL appear stacked under one date label. Dates SHALL be displayed in ascending order (earliest first).

#### Scenario: Multiple events on same date
- **WHEN** two or more events exist on the same qualifying date
- **THEN** they SHALL appear under a single date label, stacked vertically

#### Scenario: Events on multiple dates
- **WHEN** events exist on three different qualifying dates
- **THEN** the date with the earliest date SHALL appear first in the list

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
