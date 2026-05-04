## 1. Database Migration

- [x] 1.1 Add `carried_over` (Boolean, default False, not null) column to `entries` table via Alembic migration
- [x] 1.2 Add `original_date` (Date, nullable) column to `entries` table in the same migration
- [x] 1.3 Update `Entry` model in `models.py` with the two new columns

## 2. Rollover Job

- [x] 2.1 Add `carryover_incomplete_chores()` function in `scheduler.py` that queries yesterday's custom chore entries with `done=False`
- [x] 2.2 Add deduplication check: skip if a carried-over entry with same `content` already exists for today
- [x] 2.3 For each eligible entry, create new `Entry` for today with `carried_over=True` and `original_date` copied (or set to source's `date` if NULL)
- [x] 2.4 Register the job with `CronTrigger(hour=0, minute=0, timezone=config.TIMEZONE)` in the scheduler startup

## 3. Day View UI

- [x] 3.1 Pass `carried_over` and `original_date` fields through to the day view template context
- [x] 3.2 Add carryover badge HTML in the chore list template — show "↩ from <original_date>" when `carried_over=True`
- [x] 3.3 Style the badge (small, muted, distinct from the chore content text) using existing CSS patterns

## 4. Tests

- [x] 4.1 Unit test: rollover job creates correct entry for incomplete custom chore
- [x] 4.2 Unit test: rollover job skips completed chores
- [x] 4.3 Unit test: deduplication guard prevents duplicate carried-over entries
- [x] 4.4 Unit test: default chores are never touched by rollover job
- [x] 4.5 Template test: carried-over entry renders badge; non-carried-over entry does not
