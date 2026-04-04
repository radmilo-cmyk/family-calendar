## 1. Project Setup

- [x] 1.1 Create project folder structure: `app/`, `app/templates/`, `app/static/`
- [x] 1.2 Create `requirements.txt` with: fastapi, uvicorn, sqlalchemy, jinja2, python-multipart, itsdangerous, twilio, apscheduler, python-dotenv, pytz
- [x] 1.3 Create `.env` file with placeholder values for credentials (and add to `.gitignore`)
- [x] 1.4 Create `app/config.py` to load all env variables (users, Twilio credentials, phone numbers, timezone)

## 2. Database & Models

- [x] 2.1 Create `app/database.py` to set up SQLAlchemy engine and session with SQLite
- [x] 2.2 Create `app/models.py` defining the `Entry` model (id, date, type, content, author)
- [x] 2.3 Add database initialisation call so tables are created on app startup

## 3. Authentication

- [x] 3.1 Create `app/auth.py` with login logic: check username/password against config, create signed session cookie
- [x] 3.2 Create a `require_auth` dependency function that redirects unauthenticated requests to `/login`
- [x] 3.3 Create `app/templates/login.html` with a login form
- [x] 3.4 Add `/login` GET route (show form) and POST route (process login) in `app/main.py`
- [x] 3.5 Add `/logout` route that clears the session and redirects to `/login`

## 4. Calendar View

- [x] 4.1 Create `app/templates/base.html` with shared layout (nav, logout link, mobile viewport meta tag)
- [x] 4.2 Create `app/calendar_utils.py` with a function that builds a month grid (list of weeks, each a list of dates)
- [x] 4.3 Query which dates in the displayed month have entries and pass that set to the template
- [x] 4.4 Create `app/templates/calendar.html` extending base, rendering the month grid with prev/next navigation
- [x] 4.5 Add `/` route and `/calendar` route (with optional `?year=&month=` query params) in `app/main.py`

## 5. Day View & Entry Management

- [x] 5.1 Create `app/entries.py` with CRUD functions: `get_entries_for_date`, `get_entries_for_range`, `create_entry`, `delete_entry`
- [x] 5.2 Create `app/templates/day.html` extending base, showing three sections (Events, Chores, Messages) with author per entry and a delete button per entry
- [x] 5.3 Add an add-entry form at the bottom of `day.html` with a type dropdown and content textarea
- [x] 5.4 Add `/day/{date}` GET route to render the day view in `app/main.py`
- [x] 5.5 Add `/day/{date}/entries` POST route to create a new entry (validate type and non-empty content)
- [x] 5.6 Add `/entries/{entry_id}/delete` POST route to hard-delete an entry

## 6. WhatsApp Digest

- [x] 6.1 Create `app/notifications.py` with a `build_digest_message(today, tomorrow)` function that formats entries for both days into a readable WhatsApp message
- [x] 6.2 Add a `send_digest()` function in `app/notifications.py` that calls Twilio to send the message to both phone numbers; wrap in try/except and log errors
- [x] 6.3 Create `app/scheduler.py` that sets up APScheduler with `Europe/Amsterdam` timezone and schedules `send_digest` at 08:00 daily
- [x] 6.4 Start the scheduler on app startup and shut it down cleanly on app shutdown (FastAPI lifespan events)
- [x] 6.5 Add a startup check: if any Twilio env variable is missing, log a clear error and skip scheduler setup

## 7. Polish & Testing

- [x] 7.1 Add basic CSS in `app/static/style.css` for mobile-friendly layout (readable on 320px, tappable targets)
- [x] 7.2 Test the full flow locally: login → view calendar → add entries → delete an entry → logout
- [x] 7.3 Test the WhatsApp digest manually by calling `send_digest()` directly and checking both phones — requires real Twilio credentials in .env
- [x] 7.4 Verify the app runs correctly with `uvicorn app.main:app --reload`
- [x] 7.5 Create a minimal `README.md` documenting: setup steps, `.env` variables needed, how to run, Twilio sandbox opt-in instructions
