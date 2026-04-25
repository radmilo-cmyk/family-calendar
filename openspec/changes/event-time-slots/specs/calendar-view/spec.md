## MODIFIED Requirements

### Requirement: Day view displays event entries sorted by type then time
The day view SHALL display event-type entries in the following order: all-day events first (those with `time_start = NULL`), then timed events in ascending order of `time_start`. All-day events SHALL be visually marked with an "All day" badge. Timed events SHALL display their start time (and end time if present) as a label.

#### Scenario: All-day events appear before timed events
- **WHEN** a day has both all-day and timed event entries
- **THEN** all-day events SHALL render at the top of the events section
- **AND** timed events SHALL render below, ordered by `time_start` ascending

#### Scenario: All-day event badge shown
- **WHEN** an event entry has `time_start = NULL`
- **THEN** the entry card SHALL display an "All day" badge

#### Scenario: Timed event displays time label
- **WHEN** an event entry has `time_start` set
- **THEN** the entry card SHALL display the time in HH:MM format (e.g. "14:00 – 15:00" or "14:00" if no end time)

#### Scenario: Multiple timed events sorted correctly
- **WHEN** a day has timed events at 14:00, 09:00, and 11:30
- **THEN** they SHALL render in order: 09:00, 11:30, 14:00
