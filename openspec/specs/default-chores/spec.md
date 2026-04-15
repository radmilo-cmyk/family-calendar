# default-chores Specification

## Purpose
Defines the global list of default chores that appear on every day view as virtual unchecked items, and how they are managed via the settings page.

## Requirements

### Requirement: Default chores list
The system SHALL maintain a global list of default chores in a `default_chores` table. Each default chore has an `id`, `content` (text), and `position` (integer for ordering).

#### Scenario: Default chores persist across days
- **WHEN** default chores exist in the system
- **THEN** they appear on every day view, regardless of date

#### Scenario: Empty default list
- **WHEN** no default chores are configured
- **THEN** the chores section on the day view shows only user-added entries (or the empty state if none exist)

### Requirement: Manage default chores via settings page
The system SHALL provide a settings page at `/settings` where authenticated users can add and remove default chores.

#### Scenario: Access settings page
- **WHEN** an authenticated user navigates to `/settings`
- **THEN** the system displays the current list of default chores and an input form to add a new one

#### Scenario: Add a default chore
- **WHEN** a user submits the add form with non-empty content
- **THEN** the system saves a new `DefaultChore` record and redirects back to `/settings` showing the updated list

#### Scenario: Remove a default chore
- **WHEN** a user clicks the remove button next to a default chore
- **THEN** the system deletes that `DefaultChore` record and redirects back to `/settings`

#### Scenario: Unauthenticated settings access
- **WHEN** an unauthenticated request is made to `/settings`
- **THEN** the system redirects to the login page

### Requirement: Virtual rendering of default chores on day view
The system SHALL display default chores on each day view without pre-creating Entry records. A default chore is rendered as a virtual unchecked item unless a matching Entry already exists for that date.

#### Scenario: Default chore not yet acted on
- **WHEN** a day view loads and a default chore has no matching Entry for that date
- **THEN** the default chore appears as an unchecked virtual item in the Chores section

#### Scenario: Default chore already completed
- **WHEN** a day view loads and a real Entry matching a default chore exists for that date
- **THEN** the real Entry is shown (with its actual done state) rather than the virtual default item
