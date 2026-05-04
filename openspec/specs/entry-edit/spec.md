### Requirement: Edit button visible on each entry
Each entry item in the day view SHALL display a pencil (edit) icon button next to the delete button.

#### Scenario: Edit button renders
- **WHEN** the day view loads with one or more entries
- **THEN** each entry SHALL show a pencil icon button to the left of the delete button

### Requirement: Inline edit form expands on click
Clicking the edit button SHALL expand an inline form pre-filled with the entry's current values.

#### Scenario: Form opens with current values
- **WHEN** user clicks the edit button on an entry
- **THEN** an edit form SHALL appear below that entry with `content`, `author`, and `entry_type` pre-filled

#### Scenario: Only one form open at a time
- **WHEN** user clicks edit on a second entry while another edit form is open
- **THEN** the first form SHALL close and the new form SHALL open

#### Scenario: Cancel collapses form
- **WHEN** user clicks the Cancel button or presses Escape
- **THEN** the edit form SHALL collapse with no changes saved

### Requirement: Save updates the entry
Submitting the edit form SHALL persist the updated values and reload the day view.

#### Scenario: Successful edit
- **WHEN** user modifies content or author and clicks Save
- **THEN** the entry SHALL reflect the new values on the reloaded day view

#### Scenario: Empty content blocked
- **WHEN** user clears the content field and clicks Save
- **THEN** the form SHALL not submit (HTML required attribute prevents it)

### Requirement: Edit preserves entry date and type context
Editing SHALL NOT change the entry's date. Entry type MAY be changed via the edit form.

#### Scenario: Date unchanged after edit
- **WHEN** user edits content and saves
- **THEN** the entry SHALL remain on the same day view date

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
