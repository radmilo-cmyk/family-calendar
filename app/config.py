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

# Telegram — we read these but don't require them at import time.
# If they're missing, the scheduler will skip setup and log a warning.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID_USER1 = os.environ.get("TELEGRAM_CHAT_ID_USER1", "")
TELEGRAM_CHAT_ID_USER2 = os.environ.get("TELEGRAM_CHAT_ID_USER2", "")

TELEGRAM_CONFIGURED = all([
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID_USER1,
    TELEGRAM_CHAT_ID_USER2,
])
