## MODIFIED Requirements

### Requirement: Default chores list
The system SHALL maintain a global list of default chores in a `default_chores` table. Each default chore has an `id`, `content` (text), and `sort_order` (integer for display ordering). The `sort_order` column replaces the previous `position` column concept and SHALL default to 0 for new records. When fetching default chores for any purpose, the system SHALL order results by `sort_order ASC`.

#### Scenario: Default chores persist across days
- **WHEN** default chores exist in the system
- **THEN** they appear on every day view, regardless of date

#### Scenario: Empty default list
- **WHEN** no default chores are configured
- **THEN** the chores section on the day view shows only user-added entries (or the empty state if none exist)

#### Scenario: New chore gets default sort order
- **WHEN** a user adds a new default chore
- **THEN** the new chore receives a `sort_order` value equal to the current maximum `sort_order` + 1, placing it at the end of the list
