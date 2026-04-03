## Context

Brand new application. No existing codebase to migrate. Two users (a couple) managing a family schedule. The app must work comfortably on a mobile browser. Complexity should be kept low — this is also a Python learning project, so the code should be readable and teachable.

## Goals / Non-Goals

**Goals:**
- A working web app served by a Python FastAPI backend
- Jinja2 HTML templates (no separate JS framework)
- SQLite database via SQLAlchemy ORM
- Session-based auth for two hardcoded users
- Daily WhatsApp digest via Twilio at 8am, showing today + tomorrow
- Mobile-friendly layout with minimal CSS (no heavy framework needed)

**Non-Goals:**
- Multi-user registration or account management
- Native mobile app (mobile browser is sufficient)
- Real-time sync or websockets
- Recurring events or calendar integrations (Google Calendar, iCal)
- Push notifications (WhatsApp digest is enough for now)

## Decisions

### FastAPI over Flask or Django
FastAPI is modern, well-documented, and teaches clean Python patterns (type hints, Pydantic models). Flask would also work but has less structure. Django is overkill for two users and one small database.

Alternatives considered: Flask (simpler but less structured), Django (too heavy).

### SQLite over PostgreSQL
SQLite is a file — no server to run, no credentials to manage, easy to back up. At two-user scale there are no concurrency concerns. Can be swapped for PostgreSQL later with minimal code changes since SQLAlchemy abstracts the database layer.

Alternatives considered: PostgreSQL (better for scale, unnecessary here), JSON file (no query capability).

### SQLAlchemy ORM over raw SQL
Teaching moment: SQLAlchemy lets you think in Python objects rather than SQL strings. It also prevents SQL injection by default. The ORM adds a small amount of complexity but is worth it for the learning value and safety.

### Jinja2 templates over a JS frontend
Keeping everything in Python reduces cognitive load during the learning phase. Jinja2 templates are rendered server-side — the browser just receives HTML. This is how web apps worked before SPAs and is still a completely valid approach for small apps.

Alternatives considered: React (separate frontend codebase, too much context switching), HTMX (good middle ground, but adds a new concept to learn).

### APScheduler for the daily digest
APScheduler runs inside the FastAPI process — no need for a separate cron job or task queue. Simple to configure, easy to understand. At this scale (one job, twice daily) it's the right tool.

Alternatives considered: Celery + Redis (powerful but heavy), system cron (works but requires server access and separate script).

### Twilio for WhatsApp
Twilio's WhatsApp sandbox is free for development and their Python SDK is three lines of code. The main constraint is that both phone numbers must opt in to the sandbox during development. Production requires a WhatsApp Business account approval.

Alternatives considered: WhatsApp Cloud API directly (more complex setup), Telegram (different app than what the family uses).

### Data model: single `entries` table
All entry types (event, chore, message) share the same shape: date, type, content, author. A single table with a `type` column is simpler than three separate tables and makes querying by date trivial.

## Risks / Trade-offs

- **Twilio sandbox requires opt-in** → Both users must send a join message to the sandbox number before receiving messages. Mitigation: document this in the setup guide.
- **APScheduler timing depends on server being running** → If the app is down at 8am, the digest won't send. Mitigation: acceptable for a personal app; note it as a known limitation.
- **Hardcoded credentials in config** → Simple but not suitable for a public-facing app. Mitigation: store in a `.env` file excluded from git; document clearly.
- **No HTTPS by default in development** → Sessions work on HTTP locally. Mitigation: deploy behind a reverse proxy (nginx) or use a platform like Render/Railway that provides HTTPS automatically.

## Migration Plan

1. Initialize Python project with `pyproject.toml` (or `requirements.txt`)
2. Set up FastAPI app with SQLite database
3. Build auth, calendar view, day view, and entry management
4. Add Twilio integration and scheduler
5. Test locally with Twilio sandbox
6. Deploy to a simple hosting platform (Render, Railway, or a VPS)

Rollback: not applicable — greenfield project.

## Open Questions

All resolved:
- **Timezone**: `Europe/Amsterdam` — all scheduling and date display uses this timezone
- **Deleted entries**: Hard delete — removed from the database immediately, no soft-delete/archive
