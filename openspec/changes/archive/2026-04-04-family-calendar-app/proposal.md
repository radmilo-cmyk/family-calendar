## Why

Managing a family's schedule across school events, vacations, chores, and daily notes currently relies on scattered messages and memory. This app gives two people a single shared place to coordinate, with daily WhatsApp digests so nothing gets missed.

## What Changes

- New web application built with Python (FastAPI) and Jinja2 templates
- Shared calendar with monthly and day-level views
- Per-day entries in three categories: events, chores, and messages — each attributed to the person who added them
- Daily WhatsApp digest (8am) showing today + tomorrow's entries, sent to both users
- Simple authentication for two hardcoded users (no registration flow)

## Capabilities

### New Capabilities

- `user-auth`: Session-based login for two hardcoded accounts (username + password in config)
- `calendar-view`: Monthly calendar view showing days with entries; navigate between months
- `day-view`: Day detail page showing all entries for a date grouped by type (events, chores, messages), with author attribution and an add-entry form
- `entry-management`: Create and delete calendar entries; each entry has a date, type, content, and author
- `whatsapp-notifications`: Scheduled daily digest at 8am via Twilio WhatsApp API, showing today's and tomorrow's entries for both users

### Modified Capabilities

## Impact

- New Python project: FastAPI, SQLAlchemy, Jinja2, APScheduler, Twilio SDK
- SQLite database file (local, no server required)
- Twilio account required for WhatsApp integration (free sandbox for development)
- Deployable on any server or locally; accessible via mobile browser
