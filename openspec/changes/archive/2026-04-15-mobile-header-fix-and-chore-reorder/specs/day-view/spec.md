## MODIFIED Requirements

### Requirement: Day view shows all entries grouped by type
The system SHALL display a day detail page at `/day/YYYY-MM-DD` showing all entries for that date, grouped into three sections: Events, Chores, and Messages. Each entry SHALL show its content and the author who created it. The Chores section SHALL render as an interactive checklist; done chores SHALL also show the name of who completed them. Default chores not yet acted on for that date SHALL appear as virtual unchecked items in the Chores section, ordered by their `sort_order` value (ascending), before any user-added chore entries.

#### Scenario: Day with entries
- **WHEN** a user visits `/day/2026-04-03`
- **THEN** the system displays three sections (Events, Chores, Messages); the Chores section renders each chore as a checkbox item with author name; done chores show strikethrough text and a "done by [name]" label

#### Scenario: Day with no entries in a section
- **WHEN** a day has no entries of a particular type and no default chores are configured
- **THEN** that section is still shown but displays an empty state message

#### Scenario: Day with no entries at all
- **WHEN** a user visits a day that has no entries
- **THEN** all three sections are shown; the Chores section shows virtual default chore items if any are configured, otherwise an empty state message

#### Scenario: Default chores appear in user-defined order
- **WHEN** default chores are configured with a custom sort order and a user visits any day
- **THEN** default chore virtual items appear in the Chores section sorted by `sort_order ASC`
