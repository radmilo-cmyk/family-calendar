# entry-management Specification

## Purpose
TBD - created by archiving change family-calendar-app. Update Purpose after archive.
## Requirements
### Requirement: Entries are stored with date, type, content, author, and optional time slot
The system SHALL persist each entry with the following fields: a date (YYYY-MM-DD), a type (one of: event, chore, message), text content, the username of the author who created it, a `done` boolean (default False), a `done_by` string (nullable), `time_start` (TIME, nullable), and `time_end` (TIME, nullable). The `done` and `done_by` fields are only meaningful for entries of type `chore`. The `time_start` and `time_end` fields are only meaningful for entries of type `event`; for other types they SHALL always be NULL.

#### Scenario: Entry is created
- **WHEN** a valid entry is submitted
- **THEN** it is stored in the database with all fields populated; `done` defaults to False and `done_by` is null

#### Scenario: Event entry created with time slot
- **WHEN** an event entry is submitted with `time_start = "14:00"` and `time_end = "15:00"`
- **THEN** the entry SHALL be stored with those time values

#### Scenario: Chore entry ignores time fields
- **WHEN** a chore entry is submitted (even if time fields are present in the request)
- **THEN** the entry SHALL be stored with `time_start = NULL` and `time_end = NULL`

#### Scenario: Invalid type is rejected
- **WHEN** an entry is submitted with a type not in (event, chore, message)
- **THEN** the system rejects it with a validation error

### Requirement: Entries can be queried by date
The system SHALL support retrieving all entries for a given date, and all entries for a date range (used by the WhatsApp digest).

#### Scenario: Query by single date
- **WHEN** the system requests all entries for 2026-04-03
- **THEN** only entries with date 2026-04-03 are returned

#### Scenario: Query by date range
- **WHEN** the system requests entries for dates 2026-04-03 through 2026-04-04
- **THEN** all entries within that range are returned

### Requirement: Entries are hard-deleted
The system SHALL permanently remove an entry from the database when a delete request is made. No archive or soft-delete mechanism exists.

#### Scenario: Delete an entry
- **WHEN** a delete request is issued for an entry ID
- **THEN** the entry is removed from the database and cannot be retrieved

#### Scenario: Delete non-existent entry
- **WHEN** a delete request is issued for an ID that does not exist
- **THEN** the system returns a 404 response

### Requirement: Chore entries can be toggled done or undone
The system SHALL support updating the `done` and `done_by` fields of a chore entry via a toggle endpoint. Non-chore entries SHALL NOT be toggled.

#### Scenario: Toggle chore to done
- **WHEN** a toggle request is made for a chore entry where `done=False`
- **THEN** the system sets `done=True` and `done_by` to the current user

#### Scenario: Toggle chore back to undone
- **WHEN** a toggle request is made for a chore entry where `done=True`
- **THEN** the system sets `done=False` and `done_by=None`

