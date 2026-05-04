# event-recurrence Specification

## Purpose
Defines the rules and behavior for recurring events: creating a recurrence rule, expanding instances, and managing edits/deletes at single-occurrence or all-future scope.

## Requirements

### Requirement: A recurrence rule can be created for an event
The system SHALL allow a user to create a recurrence rule that causes an event to repeat on a schedule. A rule stores: `frequency` (daily, weekly, monthly), `days_of_week` (JSON array of integers 0–6, Mon=0; only used when frequency=weekly), `until_date` (YYYY-MM-DD, inclusive), `content`, `author`, `time_start` (nullable), `time_end` (nullable), and `excluded_dates` (JSON array of YYYY-MM-DD strings, initially empty).

#### Scenario: Weekly recurrence created
- **WHEN** a user submits a recurrence rule with `frequency="weekly"`, `days_of_week=[0,2]`, `until_date="2026-12-31"`, `content="Football practice"`, `author="Radmilo"`
- **THEN** the rule SHALL be persisted in the `recurrences` table and the system SHALL return the new rule's `id`

#### Scenario: Daily recurrence created
- **WHEN** a user submits a recurrence rule with `frequency="daily"` and `until_date="2026-06-01"`
- **THEN** the rule SHALL be persisted with `days_of_week=NULL`

#### Scenario: Monthly recurrence created
- **WHEN** a user submits a recurrence rule with `frequency="monthly"` and `until_date="2026-12-31"`
- **THEN** the rule SHALL be persisted with `days_of_week=NULL`

#### Scenario: Invalid frequency rejected
- **WHEN** a rule is submitted with `frequency="yearly"`
- **THEN** the system SHALL reject it with a validation error

### Requirement: Recurring event instances appear on matching dates
The system SHALL compute and return recurring event instances for any queried date that falls within the rule's range and matches its pattern, provided that date is not in `excluded_dates`.

#### Scenario: Weekly rule matches correct days
- **WHEN** a weekly rule has `days_of_week=[0,2]` (Mon, Wed) and the queried date is a Monday within the `until_date`
- **THEN** a virtual event instance SHALL be returned for that date with the rule's `content`, `author`, `time_start`, and `time_end`

#### Scenario: Weekly rule skips non-matching days
- **WHEN** a weekly rule has `days_of_week=[0]` (Mon only) and the queried date is a Tuesday
- **THEN** no instance SHALL be returned for that date from this rule

#### Scenario: Instance not returned after until_date
- **WHEN** the queried date is after the rule's `until_date`
- **THEN** no instance SHALL be returned for that date from this rule

#### Scenario: Excluded date is skipped
- **WHEN** a date is in the rule's `excluded_dates`
- **THEN** no instance SHALL be returned for that date from this rule

### Requirement: A single occurrence can be deleted without affecting the series
The system SHALL allow a user to exclude a specific occurrence of a recurring event by adding its date to the rule's `excluded_dates`. The rule itself and all other occurrences remain unchanged.

#### Scenario: Delete this occurrence
- **WHEN** user deletes a single occurrence of a recurring event on date D
- **THEN** D SHALL be added to `excluded_dates` on the rule
- **AND** the rule's other occurrences SHALL remain unaffected

### Requirement: All future occurrences can be deleted from a given date
The system SHALL allow a user to delete a recurring event from a given date D onward. The system SHALL set the rule's `until_date` to D-1 (terminating future occurrences). If D is the first occurrence, the entire rule SHALL be deleted.

#### Scenario: Delete all future occurrences
- **WHEN** user deletes all future occurrences of a rule starting from date D
- **THEN** the rule's `until_date` SHALL be updated to D-1
- **AND** occurrences before D SHALL remain visible

#### Scenario: Delete entire series (D equals first occurrence)
- **WHEN** user deletes all future occurrences starting from the rule's first occurrence date
- **THEN** the rule SHALL be hard-deleted from the database

### Requirement: A single occurrence can be edited independently
The system SHALL allow a user to modify a single occurrence of a recurring event without changing the rest of the series. The system SHALL add the occurrence's date to `excluded_dates` on the rule and create a standalone entry for that date with the modified values.

#### Scenario: Edit this occurrence
- **WHEN** user edits a single occurrence on date D with new `content="Changed content"`
- **THEN** D SHALL be added to the rule's `excluded_dates`
- **AND** a new standalone entry SHALL be created for date D with `content="Changed content"` and `is_exception=1`
- **AND** the rule and all other occurrences SHALL remain unchanged

### Requirement: All future occurrences can be edited from a given date
The system SHALL allow a user to edit all occurrences from date D onward. The system SHALL terminate the current rule at D-1 (update `until_date` to D-1) and create a new rule starting at D with the updated values. Occurrences before D are unaffected.

#### Scenario: Edit all future occurrences
- **WHEN** user edits all future occurrences starting from date D with new `content="Updated"`
- **THEN** the original rule's `until_date` SHALL be set to D-1
- **AND** a new rule SHALL be created starting at D with `content="Updated"` and the same frequency/pattern
- **AND** occurrences before D SHALL continue to show the original content
