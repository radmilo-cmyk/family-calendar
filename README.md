# Family Calendar

A shared family calendar for two people. Web app, works on mobile browser.

**Features:**
- Monthly calendar view — days with entries are highlighted
- Day view with three sections: Events, Chores, Messages
- Each entry shows who added it
- Daily WhatsApp digest at 08:00 (Amsterdam time) showing today + tomorrow

---

## Setup

### 1. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure your `.env` file

Copy `.env` and fill in your values:

```
# Your two accounts
USER1_USERNAME=radmilo
USER1_PASSWORD=your_password_here
USER2_USERNAME=ana
USER2_PASSWORD=your_password_here

# A long random string — used to sign session cookies
SECRET_KEY=some-very-long-random-string-here

# Twilio WhatsApp credentials (from console.twilio.com)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# Phone numbers that receive the digest (with country code)
PHONE_USER1=whatsapp:+31612345678
PHONE_USER2=whatsapp:+31687654321
```

### 3. Run the app

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Then open http://localhost:8000 in your browser.

---

## WhatsApp setup (Twilio sandbox)

Before you can receive messages in development, both phones must opt in:

1. Go to [console.twilio.com](https://console.twilio.com) → Messaging → Try it out → Send a WhatsApp message
2. Both phones send the join message shown there (e.g. `join <word>-<word>`) to the Twilio sandbox number
3. You'll receive a confirmation — you're now subscribed

The sandbox number is `+1 415 523 8886`. This opt-in is only needed for development. Production requires a WhatsApp Business account.

**To test the digest manually** (without waiting for 08:00):

```python
source .venv/bin/activate
python -c "from app.notifications import send_digest; send_digest()"
```

---

## Project structure

```
app/
  main.py           # FastAPI app, all routes
  config.py         # Loads .env, exposes settings
  database.py       # SQLAlchemy engine + session
  models.py         # Entry database model
  auth.py           # Login, session cookies
  entries.py        # CRUD functions for entries
  calendar_utils.py # Month grid builder
  notifications.py  # WhatsApp digest builder + sender
  scheduler.py      # APScheduler — fires digest at 08:00
  templates/        # Jinja2 HTML templates
  static/           # CSS
```
