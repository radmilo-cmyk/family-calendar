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

### Requirement: Event creation form includes a recurrence picker
When creating an event-type entry, the creation form SHALL include a collapsible "Repeat" section. When enabled, the user can configure: frequency (Daily / Weekly / Monthly), days of the week (multi-select checkboxes, shown only for Weekly), and an until date.

#### Scenario: Repeat section hidden by default
- **WHEN** user opens the event creation form
- **THEN** the "Repeat" section SHALL be collapsed and recurrence fields SHALL NOT be visible

#### Scenario: User enables repeat
- **WHEN** user toggles the "Repeat" switch on
- **THEN** the recurrence fields (frequency, until date) SHALL become visible

#### Scenario: Days of week shown only for weekly frequency
- **WHEN** user selects "Weekly" frequency
- **THEN** day-of-week checkboxes (Mon–Sun) SHALL appear

#### Scenario: Days of week hidden for daily and monthly
- **WHEN** user selects "Daily" or "Monthly" frequency
- **THEN** day-of-week checkboxes SHALL NOT be visible

#### Scenario: Recurring event created
- **WHEN** user submits the form with repeat enabled, frequency="weekly", days=[Mon, Wed], until=2026-12-31
- **THEN** a recurrence rule SHALL be created in the backend and the calendar SHALL refresh showing instances on matching days

#### Scenario: Non-recurring event unaffected
- **WHEN** user submits the form with repeat toggled off
- **THEN** a single standalone entry is created as before, with no recurrence rule

### Requirement: Edit scope modal shown for recurring event entries
When a user initiates an edit on a recurring event instance, the system SHALL display a modal asking the user to choose the edit scope before opening the edit form.

#### Scenario: Scope modal appears for recurring instance
- **WHEN** user clicks the edit button on a recurring event instance
- **THEN** a modal SHALL appear with two options: "Edit this event" and "Edit this and all future events"

#### Scenario: Edit this event — form pre-filled for single occurrence
- **WHEN** user selects "Edit this event" in the scope modal
- **THEN** the inline edit form SHALL open pre-filled with the instance's current values (content, author, time_start, time_end) and saving SHALL create an exception entry for this date only

#### Scenario: Edit all future events — form pre-filled for series
- **WHEN** user selects "Edit this and all future events" in the scope modal
- **THEN** the inline edit form SHALL open pre-filled with the rule's current values and saving SHALL terminate the old rule at D-1 and create a new rule from D with the updated values

#### Scenario: Edit scope modal not shown for standalone entries
- **WHEN** user clicks the edit button on a standalone (non-recurring) entry
- **THEN** no scope modal appears and the edit form opens directly as before

### Requirement: Delete scope modal shown for recurring event entries
When a user initiates a delete on a recurring event instance, the system SHALL display a modal asking the user to choose the delete scope.

#### Scenario: Scope modal appears for recurring instance delete
- **WHEN** user clicks the delete button on a recurring event instance
- **THEN** a modal SHALL appear with two options: "Delete this event" and "Delete this and all future events"

#### Scenario: Delete this event
- **WHEN** user selects "Delete this event"
- **THEN** the instance's date SHALL be added to the rule's `excluded_dates` and the instance SHALL disappear from the calendar

#### Scenario: Delete all future events
- **WHEN** user selects "Delete this and all future events"
- **THEN** the rule's `until_date` SHALL be set to D-1 and all instances from D onward SHALL disappear from the calendar

#### Scenario: Delete scope modal not shown for standalone entries
- **WHEN** user clicks the delete button on a standalone (non-recurring) entry
- **THEN** no scope modal appears and the entry is deleted as before
