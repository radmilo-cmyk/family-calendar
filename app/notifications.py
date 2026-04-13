import logging
import urllib.request
import urllib.parse
import json
from datetime import date, timedelta

import pytz

from app import config

logger = logging.getLogger(__name__)

ENTRY_ICONS = {"event": "📅", "chore": "🧹", "message": "💬"}


def build_digest_message(today: date, tomorrow: date) -> str:
    from app.database import SessionLocal
    from app.entries import get_entries_for_range

    db = SessionLocal()
    try:
        entries = get_entries_for_range(db, today, tomorrow)
    finally:
        db.close()

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
            for entry_type in ("event", "chore", "message"):
                typed = [e for e in day_entries if e.type == entry_type]
                for e in typed:
                    icon = ENTRY_ICONS[entry_type]
                    lines.append(f"  {icon} {e.content} _\(by {e.author}\)_")

        lines.append("")

    return "\n".join(lines).strip()


def send_telegram_message(chat_id: str, text: str) -> dict:
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "MarkdownV2",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def send_digest() -> None:
    if not config.TELEGRAM_CONFIGURED:
        logger.warning("Telegram not configured — skipping digest.")
        return

    tz = pytz.timezone(config.TIMEZONE)
    from datetime import datetime
    today = datetime.now(tz).date()
    tomorrow = today + timedelta(days=1)

    message = build_digest_message(today, tomorrow)

    for chat_id in [config.TELEGRAM_CHAT_ID_USER1, config.TELEGRAM_CHAT_ID_USER2]:
        try:
            send_telegram_message(chat_id, message)
            logger.info("Digest sent to chat_id %s", chat_id)
        except Exception as e:
            logger.error("Failed to send digest to %s: %s", chat_id, e)
