## Context

`Entry` is the core model. Custom chores are `Entry` rows with `type="chore"`. Default chores are `DefaultChore` rows rendered virtually — no `Entry` row unless acted on. The app already has a scheduled job via APScheduler + `CronTrigger` (see `scheduler.py`). The `Entry` model currently has no field to track rollover state.

## Goals / Non-Goals

**Goals:**
- Auto-copy incomplete custom chores to the next day at midnight
- Track whether an entry was carried over (for UI badge rendering)
- Preserve the original creation date for traceability
- Stop carryover once a chore is marked done

**Non-Goals:**
- Carrying over default chores (they're always virtual)
- Carrying over events or messages
- Notifying users when carryover happens
- Setting a max carryover limit (chore rolls over indefinitely until done)

## Decisions

### Decision 1: Add `carried_over` + `original_date` to `Entry`

Add two nullable columns to `Entry`:
- `carried_over: Boolean, default=False` — True when this row was created by the rollover job, not by a user directly
- `original_date: Date, nullable=True` — the date the chore was first manually added

**Why over a separate table**: The simplest model. No join needed to render the badge. The day view already queries `Entry` rows by date.

**Alternative considered**: Separate `ChoreCarryoverLog` table tracking rollover history. Rejected — overkill for the current use case.

### Decision 2: Rollover job runs at midnight via existing APScheduler

Add a new job to `scheduler.py` using `CronTrigger(hour=0, minute=0, timezone=config.TIMEZONE)`. It queries all custom chore entries for "yesterday" where `done=False`, and for each one creates a new `Entry` for "today" with `carried_over=True` and `original_date` copied from the source (or set to yesterday if the source has none).

**Why midnight**: Aligns with the day boundary. A chore undone at 23:59 rolls over at 00:00.

**Why not a lazy/on-load approach**: On-load rollover (generating carryovers when the day view is opened) is harder to reason about and risks duplicate rows if two users open the same day simultaneously.

### Decision 3: No deduplication guard needed on first pass

If the rollover job fails and is re-run, it could create duplicate entries. Mitigation: add a unique constraint or check for existing carried-over entries with the same content and date before inserting.

## Risks / Trade-offs

- **Midnight job timezone drift** → Use `config.TIMEZONE` consistently (same pattern as existing digest job)
- **Duplicate entries on job retry** → Query before insert: skip if a carried-over entry with same content already exists for that date
- **Migration on existing data** → `carried_over` defaults to False, `original_date` defaults to NULL — safe for existing rows, no data loss

## Migration Plan

1. Alembic migration: add `carried_over` (Boolean, default False, not null) and `original_date` (Date, nullable) to `entries` table
2. Deploy new scheduler job
3. No rollback complexity — new columns are additive and optional
