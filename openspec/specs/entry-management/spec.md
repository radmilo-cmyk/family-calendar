# entry-management Specification

## Purpose
TBD - created by archiving change family-calendar-app. Update Purpose after archive.
## Requirements
### Requirement: Entries are stored with date, type, content, and author
The system SHALL persist each entry with the following fields: a date (YYYY-MM-DD), a type (one of: event, chore, message), text content, and the username of the author who created it.

#### Scenario: Entry is created
- **WHEN** a valid entry is submitted
- **THEN** it is stored in the database with all four fields populated

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

