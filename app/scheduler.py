import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app import config

logger = logging.getLogger(__name__)

# Module-level scheduler instance — created once, started/stopped by main.py
_scheduler = BackgroundScheduler(timezone=config.TIMEZONE)


def start_scheduler() -> None:
    """
    Register the daily digest job and start the scheduler.
    Called once at app startup.
    """
    if not config.TELEGRAM_CONFIGURED:
        logger.warning(
            "Telegram credentials not fully configured. "
            "Digest scheduler will NOT start. "
            "Set TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID_USER1, and TELEGRAM_CHAT_ID_USER2 in your .env file."
        )
        return

    from app.notifications import send_digest

    # CronTrigger(hour=8, minute=0) fires every day at 08:00 in the scheduler's timezone.
    _scheduler.add_job(
        send_digest,
        trigger=CronTrigger(hour=8, minute=0),
        id="daily_digest",
        replace_existing=True,
    )

    _scheduler.start()
    logger.info("Digest scheduler started — daily digest at 08:00 %s.", config.TIMEZONE)


def stop_scheduler() -> None:
    """Gracefully stop the scheduler. Called on app shutdown."""
    if _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped.")
