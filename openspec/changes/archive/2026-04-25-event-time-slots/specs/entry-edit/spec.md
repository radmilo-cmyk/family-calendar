## ADDED Requirements

### Requirement: Edit form exposes time slot for event-type entries
When editing an event-type entry, the edit form SHALL display the time slot picker pre-filled with the current `time_start` and `time_end` values. The user SHALL be able to set, change, or clear the time slot. Clearing both time fields reverts the entry to all-day.

#### Scenario: Edit timed event — time picker pre-filled
- **WHEN** user opens the edit form for an event with `time_start = "10:00"` and `time_end = "11:00"`
- **THEN** the time picker fields SHALL be pre-filled with those values

#### Scenario: Edit all-day event — time picker empty
- **WHEN** user opens the edit form for an all-day event
- **THEN** both time picker fields SHALL be empty

#### Scenario: User sets time on a previously all-day event
- **WHEN** user fills in `time_start` and saves
- **THEN** the entry SHALL be stored as a timed event

#### Scenario: User clears time on a previously timed event
- **WHEN** user clears both `time_start` and `time_end` and saves
- **THEN** the entry SHALL be stored with both fields NULL (all-day)
