# event-time-slots Specification

## Purpose
Defines the optional time slot feature for event-type entries. Events may carry a start and end time; without a time slot they are classified as all-day events.

## Requirements

### Requirement: Event entries may have an optional time slot
Event-type entries SHALL support an optional time range consisting of `time_start` and `time_end`. When neither is set, the entry is classified as all-day. When `time_start` is set, the entry is classified as timed. `time_end` is optional even when `time_start` is set.

#### Scenario: All-day event created with no time
- **WHEN** a user creates an event entry without selecting a time slot
- **THEN** the entry SHALL be stored with `time_start = NULL` and `time_end = NULL`
- **AND** the entry SHALL be classified as all-day

#### Scenario: Timed event created with start time only
- **WHEN** a user creates an event entry and sets `time_start` but not `time_end`
- **THEN** the entry SHALL be stored with the given `time_start` and `time_end = NULL`
- **AND** the entry SHALL be classified as timed

#### Scenario: Timed event created with start and end time
- **WHEN** a user creates an event entry and sets both `time_start` and `time_end`
- **THEN** the entry SHALL be stored with both time values
- **AND** `time_end` SHALL be ≥ `time_start`

### Requirement: Time picker is only shown for event type entries
The time slot picker in the creation and edit forms SHALL only be visible when the entry type is set to `event`. For `chore` and `message` types the picker SHALL be hidden and no time values submitted.

#### Scenario: Type is chore — no time picker visible
- **WHEN** user selects type = chore in the entry form
- **THEN** the time slot section SHALL be hidden

#### Scenario: Type is event — time picker visible
- **WHEN** user selects type = event in the entry form
- **THEN** the time slot section SHALL become visible

### Requirement: Existing entries are migrated to all-day
All entries that exist prior to this feature being deployed SHALL be classified as all-day by setting `time_start = NULL` and `time_end = NULL`.

#### Scenario: Pre-existing event entry
- **WHEN** the database migration runs
- **THEN** all existing entries SHALL have `time_start = NULL` and `time_end = NULL`
