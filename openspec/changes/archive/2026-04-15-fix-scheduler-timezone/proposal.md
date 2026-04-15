## Why

APScheduler's `CronTrigger` does not inherit the timezone from the `BackgroundScheduler` instance — it defaults to UTC. This caused the daily Telegram digest to fire at 08:00 UTC (10:00 AM Amsterdam in summer) instead of 08:00 Amsterdam time, making it appear as if the scheduler was broken.

## What Changes

- Pass `timezone=config.TIMEZONE` explicitly to `CronTrigger` so the job fires at the correct local time
- Add a `logger.info("send_digest() triggered")` at the start of `send_digest()` for visibility in Render logs
- Wrap `build_digest_message()` in a `try/except` so build-phase errors are logged and don't silently swallow the digest

## Capabilities

### New Capabilities
<!-- None — this is a bug fix with no new user-facing capabilities -->

### Modified Capabilities
<!-- No spec-level behavior changes — the digest was always intended to fire at 08:00 Amsterdam. This fix corrects the implementation to match the existing intent. -->

## Impact

- `app/scheduler.py`: `CronTrigger` call updated
- `app/notifications.py`: `send_digest()` logging and error handling improved
- No database, API, or dependency changes
