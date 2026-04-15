## ADDED Requirements

### Requirement: Default chores can be reordered via settings page
The system SHALL provide a drag-to-reorder interface on the Default Daily Chores section of `/settings`. Saving the new order SHALL persist a `sort_order` integer on each `DefaultChore` record.

#### Scenario: User drags a chore to a new position
- **WHEN** a user drags a chore item to a different position in the list
- **THEN** the list visually reorders immediately and the new order is saved to the server

#### Scenario: Order persists after page reload
- **WHEN** a user reorders chores and reloads `/settings`
- **THEN** the chores appear in the last saved order

#### Scenario: Reorder endpoint rejects unauthenticated requests
- **WHEN** an unauthenticated request is made to the reorder endpoint
- **THEN** the system returns a 401 or redirects to login

### Requirement: Mobile header title stays left-aligned
The system SHALL display the `site-title` element on the left and the `nav` group on the right on all screen sizes, including narrow mobile viewports (≥ 320px wide).

#### Scenario: Header on narrow mobile screen
- **WHEN** a user views the app on a screen ≤ 480px wide
- **THEN** the "Family Calendar" title appears on the left and the settings cog + logout link appear on the right, on the same row

#### Scenario: Header on desktop
- **WHEN** a user views the app on a screen > 480px wide
- **THEN** the header layout is unchanged from current desktop behavior
