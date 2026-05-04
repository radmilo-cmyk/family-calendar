## MODIFIED Requirements

### Requirement: Chore completion toggle
The system SHALL allow any authenticated user to mark a chore entry as done or undo a completion. The system SHALL record which user completed the chore. The toggle SHALL be available for both user-added chores (including carried-over chores) and default chores that have been instantiated as entries. When a chore with `carried_over=True` is marked done, it SHALL remain done and SHALL NOT be picked up by the nightly rollover job on subsequent nights.

#### Scenario: Mark chore as done
- **WHEN** an authenticated user checks an unchecked chore checkbox
- **THEN** the system sets `done=True` and `done_by` to the current user's username on that entry and redirects back to the day view

#### Scenario: Undo a completion
- **WHEN** an authenticated user unchecks a checked chore checkbox
- **THEN** the system sets `done=False` and `done_by=None` on that entry and redirects back to the day view

#### Scenario: Unauthenticated toggle attempt
- **WHEN** an unauthenticated request is made to the toggle endpoint
- **THEN** the system redirects to the login page

#### Scenario: Marking a carried-over chore done stops carryover
- **WHEN** an authenticated user marks a carried-over chore as done (`done=True`)
- **THEN** the nightly rollover job does not create a new Entry for that chore the following midnight
