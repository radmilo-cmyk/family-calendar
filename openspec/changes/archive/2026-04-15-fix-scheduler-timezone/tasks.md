## 1. Scheduler Fix

- [x] 1.1 Pass `timezone=config.TIMEZONE` to `CronTrigger` in `app/scheduler.py`

## 2. Logging & Error Handling

- [x] 2.1 Add `logger.info("send_digest() triggered")` at start of `send_digest()` in `app/notifications.py`
- [x] 2.2 Wrap `build_digest_message()` in try/except and log errors in `app/notifications.py`

## 3. Deploy & Verify

- [x] 3.1 Commit and push to GitHub (triggers Render auto-deploy)
- [x] 3.2 Confirm digest arrives at 08:00 Amsterdam time the next day
