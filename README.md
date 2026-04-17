# Family Calendar
A shared household calendar for two people — log events, chores, and messages by day, and get a morning digest on Telegram.

## What it does
- Monthly calendar view with day-level highlights when entries exist
- Day view with three sections: Events, Chores, Messages — each entry shows who added it
- Default chores list shown on every day; check them off or add custom ones from Settings
- Incomplete custom chores carry over automatically at midnight so nothing gets lost
- Daily Telegram digest at 08:00 (Amsterdam time) showing today and tomorrow

## Who it's for
Two people sharing a home who want one simple place to coordinate — no separate apps, no group chats, just open the browser.

## Quick start
```bash
git clone <repo-url>
cd family-calendar
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your values
uvicorn app.main:app --reload
```
Open http://localhost:8000

## Installation

**Requirements:** Python 3.11+, optional PostgreSQL for production (SQLite used locally by default)

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage examples

**Open the calendar**
```
http://localhost:8000
```

**Add an entry**
Navigate to any day → type in the Events, Chores, or Messages field → submit.

**Trigger the Telegram digest manually** (without waiting for 08:00)
```
GET http://localhost:8000/debug/send-digest
```
Returns JSON with send results and a message preview.

## Configuration / environment variables

| Variable | Required | Description | Example |
|---|---|---|---|
| `USER1_USERNAME` | Yes | Login username for person 1 | `radmilo` |
| `USER1_PASSWORD` | Yes | Password for person 1 | `yourpassword` |
| `USER2_USERNAME` | Yes | Login username for person 2 | `ana` |
| `USER2_PASSWORD` | Yes | Password for person 2 | `yourpassword` |
| `SECRET_KEY` | Yes | Long random string — signs session cookies | `some-very-long-random-string` |
| `DATABASE_URL` | No | PostgreSQL URI for production; defaults to SQLite locally | `postgresql://user:pass@host/db` |
| `TELEGRAM_BOT_TOKEN` | No | Bot token from BotFather — digest skipped if missing | `123456:ABC-DEF1234...` |
| `TELEGRAM_CHAT_ID_USER1` | No | Telegram chat ID for person 1 | `123456789` |
| `TELEGRAM_CHAT_ID_USER2` | No | Telegram chat ID for person 2 | `987654321` |

> Telegram vars are optional. If any are missing, the digest job is skipped at startup with a warning — everything else works normally.

## Project structure

```
app/
  main.py              # FastAPI app — all routes
  config.py            # Loads .env, exposes settings
  database.py          # SQLAlchemy engine + session (SQLite locally, PostgreSQL in prod)
  models.py            # Entry + DefaultChore database models
  auth.py              # Login, session cookies
  entries.py           # CRUD functions for entries
  calendar_utils.py    # Month grid builder
  default_chores.py    # Default chores CRUD + in-memory cache
  notifications.py     # Telegram digest builder + sender (Bot API via urllib)
  scheduler.py         # APScheduler — midnight carryover + 08:00 Telegram digest
  templates/           # Jinja2 HTML templates
  static/              # CSS, favicon
tests/
  test_carryover.py    # Chore carryover tests
```

## Development workflow

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

App runs at http://localhost:8000. SQLite database is created as `calendar.db` on first run — no migration needed locally.

Scheduled jobs run automatically:
- `00:00` — rolls incomplete custom chores to the next day
- `08:00` — sends Telegram digest to both users (only if Telegram is configured)

## Testing

```bash
source .venv/bin/activate
pytest tests/
```

Currently covers: chore carryover logic (`tests/test_carryover.py`).

## Deployment

Deploy to any VPS or platform (Render, Railway, Fly.io) with Python 3.11+:

1. Set `DATABASE_URL` to your PostgreSQL URI (Supabase works)
2. Set all required env vars
3. Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

> `twilio` is listed in `requirements.txt` as a leftover from an earlier version — it is not used and can be removed.

## License

MIT
