from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from app.config import SECRET_KEY, USERS

# The serializer signs and verifies session cookies using the secret key.
# "session" is just a label (called a "salt") to namespace our cookies.
_serializer = URLSafeTimedSerializer(SECRET_KEY, salt="session")


def create_session_cookie(username: str) -> str:
    """Turn a username into a signed cookie value the browser will store."""
    return _serializer.dumps({"user": username})


def get_current_user(request: Request) -> str | None:
    """
    Read the session cookie from the request and return the username.
    Returns None if the cookie is missing, expired, or tampered with.
    """
    token = request.cookies.get("session")
    if not token:
        return None
    try:
        # max_age=86400 means the session expires after 24 hours (in seconds).
        data = _serializer.loads(token, max_age=86400 * 30)
        return data.get("user")
    except (BadSignature, SignatureExpired):
        return None


def require_auth(request: Request) -> str:
    """
    FastAPI dependency: ensures the user is logged in.
    If not, redirects to /login.
    Raise HTTPException so FastAPI knows to stop processing the route.
    """
    user = get_current_user(request)
    if not user:
        # We use a special exception to trigger a redirect response.
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user


def check_credentials(username: str, password: str) -> bool:
    """Return True if the username/password match our configured accounts."""
    return USERS.get(username) == password
