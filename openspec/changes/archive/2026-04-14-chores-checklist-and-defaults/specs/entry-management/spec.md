## MODIFIED Requirements

### Requirement: Entries are stored with date, type, content, and author
The system SHALL persist each entry with the following fields: a date (YYYY-MM-DD), a type (one of: event, chore, message), text content, the username of the author who created it, a `done` boolean (default False), and a `done_by` string (nullable). The `done` and `done_by` fields are only meaningful for entries of type `chore`.

#### Scenario: Entry is created
- **WHEN** a valid entry is submitted
- **THEN** it is stored in the database with all fields populated; `done` defaults to False and `done_by` is null

#### Scenario: Invalid type is rejected
- **WHEN** an entry is submitted with a type not in (event, chore, message)
- **THEN** the system rejects it with a validation error

## ADDED Requirements

### Requirement: Chore entries can be toggled done or undone
The system SHALL support updating the `done` and `done_by` fields of a chore entry via a toggle endpoint. Non-chore entries SHALL NOT be toggled.

#### Scenario: Toggle chore to done
- **WHEN** a toggle request is made for a chore entry where `done=False`
- **THEN** the system sets `done=True` and `done_by` to the current user

#### Scenario: Toggle chore back to undone
- **WHEN** a toggle request is made for a chore entry where `done=True`
- **THEN** the system sets `done=False` and `done_by=None`
