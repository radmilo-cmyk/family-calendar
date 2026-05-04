## MODIFIED Requirements

### Requirement: Entries are stored with date, type, content, author, and optional time slot
The system SHALL persist each entry with the following fields: a date (YYYY-MM-DD), a type (one of: event, chore, message), text content, the username of the author who created it, a `done` boolean (default False), a `done_by` string (nullable), `time_start` (TIME, nullable), `time_end` (TIME, nullable), `recurrence_id` (INTEGER, nullable FK to `recurrences.id`), and `is_exception` (INTEGER, default 0). The `done` and `done_by` fields are only meaningful for entries of type `chore`. The `time_start` and `time_end` fields are only meaningful for entries of type `event`; for other types they SHALL always be NULL. The `recurrence_id` and `is_exception` fields are only meaningful for event entries that were created as overrides for a recurring series occurrence.

#### Scenario: Entry is created
- **WHEN** a valid entry is submitted
- **THEN** it is stored in the database with all fields populated; `done` defaults to False, `done_by` is null, `recurrence_id` is null, and `is_exception` is 0

#### Scenario: Event entry created with time slot
- **WHEN** an event entry is submitted with `time_start = "14:00"` and `time_end = "15:00"`
- **THEN** the entry SHALL be stored with those time values

#### Scenario: Chore entry ignores time fields
- **WHEN** a chore entry is submitted (even if time fields are present in the request)
- **THEN** the entry SHALL be stored with `time_start = NULL` and `time_end = NULL`

#### Scenario: Invalid type is rejected
- **WHEN** an entry is submitted with a type not in (event, chore, message)
- **THEN** the system rejects it with a validation error

#### Scenario: Exception entry stored with recurrence reference
- **WHEN** a single occurrence override is created for recurrence rule ID 5 on date 2026-06-10
- **THEN** the entry SHALL be stored with `recurrence_id=5` and `is_exception=1`

### Requirement: Entries can be queried by date
The system SHALL support retrieving all entries for a given date, and all entries for a date range (used by the WhatsApp digest). Query results SHALL include both standalone entries and computed recurring event instances for the requested date(s).

#### Scenario: Query by single date
- **WHEN** the system requests all entries for 2026-04-03
- **THEN** only entries with date 2026-04-03 are returned, plus any recurring event instances that apply to that date

#### Scenario: Query by date range
- **WHEN** the system requests entries for dates 2026-04-03 through 2026-04-04
- **THEN** all entries within that range are returned, plus recurring event instances for all dates in the range

#### Scenario: Excluded recurrence date not included
- **WHEN** a date is in a rule's `excluded_dates`
- **THEN** no instance from that rule SHALL be included in the query result for that date

## ADDED Requirements

### Requirement: Recurring event instances are returned as virtual entries
When the system queries entries for a date, it SHALL compute which recurrence rules produce an instance on that date (matching frequency, pattern, within `until_date`, and not in `excluded_dates`) and include them in the response as virtual event entries alongside stored entries. Virtual instances SHALL carry the rule's `id` as a `recurrence_id` field so the frontend can identify them as recurring.

#### Scenario: Recurring instance appears in date query
- **WHEN** a weekly rule covers Mondays and 2026-06-08 is a Monday within the rule's range
- **THEN** the query for 2026-06-08 SHALL return a virtual event with the rule's content, author, time_start, time_end, and `recurrence_id`

#### Scenario: Non-recurring entries unaffected
- **WHEN** a date has only standalone entries (no recurrence rules match)
- **THEN** the query result is identical to the pre-recurrence behavior
