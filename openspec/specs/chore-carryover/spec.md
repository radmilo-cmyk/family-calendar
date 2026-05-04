# chore-carryover Specification

## Purpose
Defines the midnight rollover job that carries incomplete custom chores forward to the next day, and the data model fields that support it.

## Requirements

### Requirement: Carryover fields on Entry
The `Entry` model SHALL include two fields to track carryover state: `carried_over` (Boolean, default False) and `original_date` (Date, nullable). These fields are only meaningful for chore-type entries.

#### Scenario: New user-added chore has no carryover markers
- **WHEN** a user manually adds a new chore entry
- **THEN** `carried_over` is False and `original_date` is NULL on the created Entry

### Requirement: Midnight rollover job for incomplete custom chores
The system SHALL run a scheduled job at midnight (in the configured timezone) that finds all `Entry` rows with `type="chore"`, `done=False`, and `date` equal to the previous day (yesterday). For each such entry, if no carried-over entry with the same `content` already exists for today, the system SHALL create a new `Entry` for today with `carried_over=True` and `original_date` set to the source entry's `original_date` (or source's `date` if `original_date` is NULL).

#### Scenario: Incomplete custom chore carries over
- **WHEN** midnight arrives and a custom chore Entry from yesterday has `done=False`
- **THEN** a new Entry is created for today with the same `content`, `author`, `type="chore"`, `done=False`, `carried_over=True`, and `original_date` equal to the original creation date

#### Scenario: Completed custom chore does not carry over
- **WHEN** midnight arrives and a custom chore Entry from yesterday has `done=True`
- **THEN** no new Entry is created for that chore

#### Scenario: Already carried over today (deduplication guard)
- **WHEN** midnight arrives and a carried-over entry with the same `content` already exists for today
- **THEN** the job does not create a duplicate entry

#### Scenario: Default chores are not affected
- **WHEN** midnight arrives
- **THEN** the job does not create entries for virtual default chores (those only in the `DefaultChore` table, not yet instantiated as entries)
