# day-view Specification

## Purpose
TBD - created by archiving change family-calendar-app. Update Purpose after archive.
## Requirements
### Requirement: Day view shows all entries grouped by type
The system SHALL display a day detail page at `/day/YYYY-MM-DD` showing all entries for that date, grouped into three sections: Events, Chores, and Messages. Each entry SHALL show its content and the author who created it. The Chores section SHALL render as an interactive checklist; done chores SHALL also show the name of who completed them. Default chores not yet acted on for that date SHALL appear as virtual unchecked items in the Chores section, ordered by their `sort_order` value (ascending), before any user-added chore entries.

#### Scenario: Day with entries
- **WHEN** a user visits `/day/2026-04-03`
- **THEN** the system displays three sections (Events, Chores, Messages); the Chores section renders each chore as a checkbox item with author name; done chores show strikethrough text and a "done by [name]" label

#### Scenario: Day with no entries in a section
- **WHEN** a day has no entries of a particular type and no default chores are configured
- **THEN** that section is still shown but displays an empty state message

#### Scenario: Day with no entries at all
- **WHEN** a user visits a day that has no entries
- **THEN** all three sections are shown; the Chores section shows virtual default chore items if any are configured, otherwise an empty state message

#### Scenario: Default chores appear in user-defined order
- **WHEN** default chores are configured with a custom sort order and a user visits any day
- **THEN** default chore virtual items appear in the Chores section sorted by `sort_order ASC`

### Requirement: User can add a new entry from the day view
The system SHALL provide an inline form on the day view page for adding a new entry. The form SHALL include a type selector (event / chore / message) and a text content field. The date is taken from the URL; the author is taken from the session.

#### Scenario: Add an entry
- **WHEN** a user fills in the add-entry form and submits
- **THEN** the new entry appears in the correct section with the user's name as author

#### Scenario: Submit empty content
- **WHEN** a user submits the form with an empty content field
- **THEN** the system shows a validation error and does not create an entry

### Requirement: User can delete any entry on the day view
The system SHALL show a delete control next to each entry. Any authenticated user MAY delete any entry (no ownership restriction).

#### Scenario: Delete an entry
- **WHEN** a user clicks delete on an entry and confirms
- **THEN** the entry is permanently removed and no longer appears on the page

### Requirement: Day view links back to the calendar
The system SHALL provide a navigation link from the day view back to the monthly calendar.

#### Scenario: Back to calendar
- **WHEN** a user clicks the back link on a day view
- **THEN** the system navigates to the monthly calendar view

