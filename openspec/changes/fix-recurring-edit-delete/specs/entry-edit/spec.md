## MODIFIED Requirements

### Requirement: Edit scope modal shown for recurring event entries
When a user initiates an edit on a recurring event instance, the system SHALL display a modal asking the user to choose the edit scope before opening the edit form. The modal trigger SHALL work regardless of special characters in the event content or author name.

#### Scenario: Scope modal appears for recurring instance
- **WHEN** user clicks the edit button on a recurring event instance
- **THEN** a modal SHALL appear with two options: "Edit this event" and "Edit this and all future events"

#### Scenario: Scope modal works with special characters in content
- **WHEN** the recurring event content contains double quotes or HTML characters
- **THEN** the edit button SHALL still open the modal correctly

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
When a user initiates a delete on a recurring event instance, the system SHALL display a modal asking the user to choose the delete scope. The modal trigger SHALL work regardless of special characters in the event content or author name.

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
