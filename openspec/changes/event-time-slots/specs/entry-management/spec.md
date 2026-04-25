## MODIFIED Requirements

### Requirement: Entries are stored with date, type, content, author, and optional time slot
The system SHALL persist each entry with the following fields: a date (YYYY-MM-DD), a type (one of: event, chore, message), text content, the username of the author who created it, a `done` boolean (default False), a `done_by` string (nullable), `time_start` (TIME, nullable), and `time_end` (TIME, nullable). The `done` and `done_by` fields are only meaningful for entries of type `chore`. The `time_start` and `time_end` fields are only meaningful for entries of type `event`; for other types they SHALL always be NULL.

#### Scenario: Event entry created with time slot
- **WHEN** an event entry is submitted with `time_start = "14:00"` and `time_end = "15:00"`
- **THEN** the entry SHALL be stored with those time values

#### Scenario: Chore entry ignores time fields
- **WHEN** a chore entry is submitted (even if time fields are present in the request)
- **THEN** the entry SHALL be stored with `time_start = NULL` and `time_end = NULL`

#### Scenario: Invalid type is rejected
- **WHEN** an entry is submitted with a type not in (event, chore, message)
- **THEN** the system rejects it with a validation error
