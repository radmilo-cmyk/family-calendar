import logging
from datetime import date, timedelta

import pytz
from twilio.rest import Client

from app import config

logger = logging.getLogger(__name__)

ENTRY_ICONS = {"event": "📅", "chore": "🧹", "message": "💬"}


def build_digest_message(today: date, tomorrow: date) -> str:
    """
    Build the WhatsApp digest text for today and tomorrow.
    We import get_entries_for_range here (inside the function) to avoid
    circular imports — notifications.py and entries.py don't need to know
    about each other at module load time.
    """
    from app.database import SessionLocal
    from app.entries import get_entries_for_range

    db = SessionLocal()
    try:
        entries = get_entries_for_range(db, today, tomorrow)
    finally:
        db.close()

    # Group entries by date
    by_date: dict[date, list] = {today: [], tomorrow: []}
    for entry in entries:
        if entry.date in by_date:
            by_date[entry.date].append(entry)

    lines = ["*🗓 Family Calendar Digest*\n"]

    for day, label in [(today, "Today"), (tomorrow, "Tomorrow")]:
        day_entries = by_date[day]
        lines.append(f"*{label} — {day.strftime('%A, %b %d')}*")

        if not day_entries:
            lines.append("  All clear ✨")
        else:
            # Group by type within the day
            for entry_type in ("event", "chore", "message"):
                typed = [e for e in day_entries if e.type == entry_type]
                for e in typed:
                    icon = ENTRY_ICONS[entry_type]
                    lines.append(f"  {icon} {e.content} _(by {e.author})_")

        lines.append("")  # blank line between days

    return "\n".join(lines).strip()


def send_digest() -> None:
    """
    Send the daily digest to both configured phone numbers.
    Called by the scheduler at 08:00 Amsterdam time.
    """
    if not config.TWILIO_CONFIGURED:
        logger.warning("Twilio not configured — skipping digest.")
        return

    tz = pytz.timezone(config.TIMEZONE)
    from datetime import datetime
    today = datetime.now(tz).date()
    tomorrow = today + timedelta(days=1)

    message = build_digest_message(today, tomorrow)

    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

    for phone in [config.PHONE_USER1, config.PHONE_USER2]:
        try:
            client.messages.create(
                from_=config.TWILIO_WHATSAPP_FROM,
                to=phone,
                body=message,
            )
            logger.info("Digest sent to %s", phone)
        except Exception as e:
            # Log the error but keep going — we still want to try the second number.
            logger.error("Failed to send digest to %s: %s", phone, e)
