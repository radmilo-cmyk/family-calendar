import os
from dotenv import load_dotenv

# Load values from the .env file into environment variables
load_dotenv()


def _require(key: str) -> str:
    """Read an environment variable, raise an error if it's missing."""
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


# App
SECRET_KEY = _require("SECRET_KEY")
TIMEZONE = "Europe/Amsterdam"

# Hardcoded user accounts: {username: password}
USERS = {
    _require("USER1_USERNAME"): _require("USER1_PASSWORD"),
    _require("USER2_USERNAME"): _require("USER2_PASSWORD"),
}

# Twilio — we read these but don't require them at import time.
# If they're missing, the scheduler will skip setup and log a warning.
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM", "")
PHONE_USER1 = os.environ.get("PHONE_USER1", "")
PHONE_USER2 = os.environ.get("PHONE_USER2", "")

TWILIO_CONFIGURED = all([
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_FROM,
    PHONE_USER1,
    PHONE_USER2,
])
