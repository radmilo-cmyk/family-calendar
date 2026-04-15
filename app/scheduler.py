import logging
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app import config

logger = logging.getLogger(__name__)

# Module-level scheduler instance — created once, started/stopped by main.py
_scheduler = BackgroundScheduler(timezone=config.TIMEZONE)


def carryover_incomplete_chores() -> None:
    """
    Runs at midnight. Finds all custom chore entries from yesterday that are
    not done, and copies them to today so they don't get lost.
    Only affects user-added chores (Entry rows) — default chores are always
    virtual and unaffected.
    """
    from app.database import SessionLocal
    from app.models import Entry

    tz = pytz.timezone(config.TIMEZONE)
    today = datetime.now(tz).date()
    yesterday = today - timedelta(days=1)

    db = SessionLocal()
    try:
        # All undone custom chores from yesterday
        pending = (
            db.query(Entry)
            .filter(
                Entry.date == yesterday,
                Entry.type == "chore",
                Entry.done == False,  # noqa: E712
            )
            .all()
        )

        # Contents already carried over to today (deduplication guard)
        existing_today = {
            e.content.lower()
            for e in db.query(Entry).filter(
                Entry.date == today,
                Entry.type == "chore",
                Entry.carried_over == True,  # noqa: E712
            ).all()
        }

        carried = 0
        for entry in pending:
            if entry.content.lower() in existing_today:
                continue  # skip duplicates

            orig = entry.original_date or entry.date
            new_entry = Entry(
                date=today,
                type="chore",
                content=entry.content,
                author=entry.author,
                done=False,
                carried_over=True,
                original_date=orig,
            )
            db.add(new_entry)
            existing_today.add(entry.content.lower())
            carried += 1

        db.commit()
        logger.info("Carryover job complete — %d chore(s) moved to %s.", carried, today)
    except Exception:
        db.rollback()
        logger.exception("Carryover job failed.")
    finally:
        db.close()


def start_scheduler() -> None:
    """
    Register scheduled jobs and start the scheduler.
    Called once at app startup.
    """
    # Midnight carryover runs regardless of Telegram config.
    _scheduler.add_job(
        carryover_incomplete_chores,
        trigger=CronTrigger(hour=0, minute=0, timezone=config.TIMEZONE),
        id="midnight_carryover",
        replace_existing=True,
    )

    if not config.TELEGRAM_CONFIGURED:
        logger.warning(
            "Telegram credentials not fully configured. "
            "Digest scheduler will NOT start. "
            "Set TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID_USER1, and TELEGRAM_CHAT_ID_USER2 in your .env file."
        )
    else:
        from app.notifications import send_digest

        # CronTrigger(hour=8, minute=0) fires every day at 08:00 in the scheduler's timezone.
        _scheduler.add_job(
            send_digest,
            trigger=CronTrigger(hour=8, minute=0, timezone=config.TIMEZONE),
            id="daily_digest",
            replace_existing=True,
        )
        logger.info("Digest scheduler started — daily digest at 08:00 %s.", config.TIMEZONE)

    _scheduler.start()
    logger.info("Scheduler started — midnight carryover active (%s).", config.TIMEZONE)


def stop_scheduler() -> None:
    """Gracefully stop the scheduler. Called on app shutdown."""
    if _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped.")
