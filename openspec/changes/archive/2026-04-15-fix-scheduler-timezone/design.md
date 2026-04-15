## Context

The daily digest scheduler uses APScheduler's `BackgroundScheduler` initialized with `timezone="Europe/Amsterdam"`. However, `CronTrigger` does not inherit the scheduler's timezone — it defaults to UTC unless explicitly told otherwise. The app runs on Render (UTC server time), so the job was silently firing 2 hours late.

The `send_digest()` function had no log at entry, making it impossible to confirm via Render's log stream whether the job ever ran.

## Goals / Non-Goals

**Goals:**
- Digest fires at 08:00 Europe/Amsterdam every day
- Render logs show a clear trace when the job runs or fails

**Non-Goals:**
- Changing the digest schedule or content
- Adding retry logic or persistent job state
- Switching to an external cron service

## Decisions

**Pass `timezone` explicitly to `CronTrigger`**
APScheduler docs state CronTrigger defaults to UTC regardless of the scheduler's timezone. Passing `timezone=config.TIMEZONE` directly to `CronTrigger` is the correct fix. Alternative (setting `TZ` env var on Render) was rejected — implicit and fragile.

**Add entry log to `send_digest()`**
A single `logger.info("send_digest() triggered")` at function entry makes Render logs actionable. Without it, there's no way to distinguish "job didn't run" from "job ran but failed silently".

**Wrap `build_digest_message()` in try/except**
Previously, an exception during message build would propagate up to APScheduler, which swallows it without surfacing it in Render logs. Catching it explicitly and logging the error gives visibility.

## Risks / Trade-offs

- No risks. Both changes are additive and the fix is a one-line correction to a misconfigured argument.

## Migration Plan

1. Deploy to Render — auto-deploy via GitHub push
2. Verify "Digest scheduler started" appears in Render boot logs
3. Verify digest arrives at 08:00 Amsterdam time next day
