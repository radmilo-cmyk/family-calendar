## Why

Custom chores added by users disappear at end of day if not marked done — there's no way to track them across days. Default chores always reappear, but manually added chores are silently lost, causing family tasks to fall through the cracks.

## What Changes

- Custom (user-added) chores not marked done by end of day automatically carry over to the next day
- Carried-over chores are visually distinguished in the UI (e.g. a "rolled over" badge or indicator)
- A chore carries over repeatedly until it is marked done
- Default chores are unaffected — they always appear on every day regardless of done state
- The original date a chore was first created is preserved for reference

## Capabilities

### New Capabilities
- `chore-carryover`: Defines the rollover logic — when and how incomplete custom chores are moved to the next day, including the data model for tracking carryover state and the scheduled job or trigger that performs the rollover
- `chore-carryover-ux`: Defines the visual treatment of carried-over chores in the day view — badge, label, or icon that distinguishes a moved chore from a freshly added one

### Modified Capabilities
- `chore-completion`: Completing a custom chore must stop its carryover chain — marking done prevents it from rolling over again

## Impact

- `Entry` model: needs `carried_over` boolean flag and `original_date` field
- New scheduled job (or trigger via existing CronTrigger pattern) to roll over entries at midnight
- Day view template: render carried-over badge on matching entries
- `chore-completion` toggle: no structural change, but done=True must halt future carryover
