# chore-completion Specification

## Purpose
Defines how chore entries can be marked as done or undone by authenticated users, including both user-added chores and virtual default chores.

## Requirements

### Requirement: Chore completion toggle
The system SHALL allow any authenticated user to mark a chore entry as done or undo a completion. The system SHALL record which user completed the chore. The toggle SHALL be available for both user-added chores and default chores that have been instantiated as entries.

#### Scenario: Mark chore as done
- **WHEN** an authenticated user checks an unchecked chore checkbox
- **THEN** the system sets `done=True` and `done_by` to the current user's username on that entry and redirects back to the day view

#### Scenario: Undo a completion
- **WHEN** an authenticated user unchecks a checked chore checkbox
- **THEN** the system sets `done=False` and `done_by=None` on that entry and redirects back to the day view

#### Scenario: Unauthenticated toggle attempt
- **WHEN** an unauthenticated request is made to the toggle endpoint
- **THEN** the system redirects to the login page

### Requirement: Complete a virtual default chore
The system SHALL allow a user to check a virtual default chore (one not yet saved as an Entry for that day). A single action SHALL create the entry AND mark it done.

#### Scenario: Checking a virtual default
- **WHEN** an authenticated user checks a virtual default chore checkbox
- **THEN** the system creates a new Entry with `type=chore`, `content` matching the default, `done=True`, `done_by=current_user`, and the current day's date, then redirects back to the day view
