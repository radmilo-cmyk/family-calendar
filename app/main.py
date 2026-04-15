from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import engine, get_db, Base
from app.auth import check_credentials, create_session_cookie, require_auth, get_current_user

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code here runs once when the app starts (before 'yield')
    and once when it shuts down (after 'yield').
    """
    # Create all database tables defined in our models (if they don't exist yet).
    # We import models here so SQLAlchemy knows about the Entry table.
    import app.models  # noqa: F401 — registers Entry + DefaultChore with SQLAlchemy
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ready.")

    # Start the digest scheduler
    from app.scheduler import start_scheduler, stop_scheduler
    start_scheduler()

    yield  # <-- app runs here

    stop_scheduler()


app = FastAPI(lifespan=lifespan)

# Serve files from app/static/ at the /static URL path
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Tell FastAPI where to find our HTML templates
templates = Jinja2Templates(directory="app/templates")


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Show the login form. If already logged in, go straight to calendar."""
    if get_current_user(request):
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse(request, "login.html")


@app.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    """
    Process the login form.
    Form(...) tells FastAPI to read 'username' and 'password' from the POST body.
    """
    if not username or not password:
        return templates.TemplateResponse(
            request, "login.html",
            {"error": "Please enter username and password."},
            status_code=400,
        )

    if not check_credentials(username, password):
        return templates.TemplateResponse(
            request, "login.html",
            {"error": "Invalid username or password."},
            status_code=401,
        )

    # Credentials valid — create a session cookie and redirect to the calendar.
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(
        key="session",
        value=create_session_cookie(username),
        httponly=True,   # JS cannot read this cookie (security best practice)
        max_age=86400 * 30,
        samesite="lax",
    )
    return response


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/debug/send-digest")
async def debug_send_digest():
    """Manually trigger the Telegram digest with full error reporting."""
    from app import config
    from app.notifications import build_digest_message, send_telegram_message
    from datetime import datetime, timedelta
    import traceback
    import pytz

    results = {
        "telegram_configured": config.TELEGRAM_CONFIGURED,
        "chat_id_user1": config.TELEGRAM_CHAT_ID_USER1,
        "chat_id_user2": config.TELEGRAM_CHAT_ID_USER2,
        "sends": [],
    }

    if not config.TELEGRAM_CONFIGURED:
        return {"status": "error", "reason": "TELEGRAM_CONFIGURED is False", **results}

    tz = pytz.timezone(config.TIMEZONE)
    today = datetime.now(tz).date()
    tomorrow = today + timedelta(days=1)

    try:
        message = build_digest_message(today, tomorrow)
        results["message_preview"] = message[:200]
    except Exception as e:
        return {"status": "error", "stage": "build_message", "error": str(e), "traceback": traceback.format_exc()}

    for chat_id in [config.TELEGRAM_CHAT_ID_USER1, config.TELEGRAM_CHAT_ID_USER2]:
        try:
            resp = send_telegram_message(chat_id, message)
            results["sends"].append({"chat_id": chat_id, "ok": resp.get("ok")})
        except Exception as e:
            results["sends"].append({"chat_id": chat_id, "error": str(e), "traceback": traceback.format_exc()})

    return results


@app.get("/logout")
async def logout():
    """Clear the session cookie and go back to login."""
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("session")
    return response


# ---------------------------------------------------------------------------
# Calendar routes (added in next tasks)
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def calendar_root(
    request: Request,
    year: int = None,
    month: int = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from app.calendar_utils import build_month_grid, get_year_month
    from app.entries import get_dates_with_entries
    import pytz
    from datetime import datetime

    tz = pytz.timezone("Europe/Amsterdam")
    now = datetime.now(tz)
    year = year or now.year
    month = month or now.month

    grid = build_month_grid(year, month)
    dates_with_entries = get_dates_with_entries(db, year, month)

    prev_year, prev_month = get_year_month(year, month, -1)
    next_year, next_month = get_year_month(year, month, +1)

    return templates.TemplateResponse(request, "calendar.html", {
        "current_user": current_user,
        "year": year,
        "month": month,
        "grid": grid,
        "dates_with_entries": dates_with_entries,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "today": now.date(),
    })


# ---------------------------------------------------------------------------
# Day view routes (added in task 5)
# ---------------------------------------------------------------------------

@app.get("/day/{date_str}", response_class=HTMLResponse)
async def day_view(
    request: Request,
    date_str: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from datetime import date
    from app.entries import get_entries_for_date
    from app.default_chores import get_all_default_chores

    try:
        day = date.fromisoformat(date_str)
    except ValueError:
        return RedirectResponse("/", status_code=302)

    entries = get_entries_for_date(db, day)
    events = [e for e in entries if e.type == "event"]
    chores = [e for e in entries if e.type == "chore"]
    messages = [e for e in entries if e.type == "message"]

    # Build virtual defaults: defaults not already present in real chores (case-insensitive match).
    real_chore_contents = {c.content.lower() for c in chores}
    all_defaults = get_all_default_chores(db)
    virtual_defaults = [d for d in all_defaults if d.content.lower() not in real_chore_contents]

    return templates.TemplateResponse(request, "day.html", {
        "current_user": current_user,
        "day": day,
        "events": events,
        "chores": chores,
        "messages": messages,
        "virtual_defaults": virtual_defaults,
    })


@app.post("/day/{date_str}/entries")
async def add_entry(
    date_str: str,
    entry_type: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from datetime import date
    from app.entries import create_entry

    if entry_type not in ("event", "chore", "message"):
        return RedirectResponse(f"/day/{date_str}?error=invalid_type", status_code=302)
    if not content.strip():
        return RedirectResponse(f"/day/{date_str}?error=empty", status_code=302)

    try:
        day = date.fromisoformat(date_str)
    except ValueError:
        return RedirectResponse("/", status_code=302)

    create_entry(db, day=day, entry_type=entry_type, content=content.strip(), author=current_user)
    return RedirectResponse(f"/day/{date_str}", status_code=302)


@app.post("/entries/{entry_id}/delete")
async def delete_entry_route(
    entry_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from app.entries import delete_entry, get_entry
    entry = get_entry(db, entry_id)
    if entry is None:
        return RedirectResponse("/", status_code=302)
    date_str = entry.date.isoformat()
    delete_entry(db, entry_id)
    return RedirectResponse(f"/day/{date_str}", status_code=302)


@app.post("/entries/{entry_id}/edit")
async def edit_entry_route(
    entry_id: int,
    entry_type: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from app.entries import update_entry, get_entry
    entry = get_entry(db, entry_id)
    if entry is None:
        return RedirectResponse("/", status_code=302)
    if entry_type not in ("event", "chore", "message") or not content.strip():
        return RedirectResponse(f"/day/{entry.date.isoformat()}", status_code=302)
    date_str = entry.date.isoformat()
    update_entry(db, entry_id, content=content.strip(), author=author.strip() or current_user, entry_type=entry_type)
    return RedirectResponse(f"/day/{date_str}", status_code=302)


@app.post("/entries/{entry_id}/toggle")
async def toggle_chore_route(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from app.entries import toggle_chore_done, get_entry, delete_entry
    from app.default_chores import get_all_default_chores
    entry = get_entry(db, entry_id)
    if entry is None:
        return RedirectResponse("/", status_code=302)
    date_str = entry.date.isoformat()

    # If unchecking a chore that matches a default, delete it entirely so it
    # returns to virtual state instead of becoming a stray regular chore.
    if entry.done:
        default_contents = {d.content.lower() for d in get_all_default_chores(db)}
        if entry.content.lower() in default_contents:
            delete_entry(db, entry_id)
            return RedirectResponse(f"/day/{date_str}", status_code=302)

    toggle_chore_done(db, entry_id, current_user)
    return RedirectResponse(f"/day/{date_str}", status_code=302)


@app.post("/day/{date_str}/chores/complete-default")
async def complete_default_chore_route(
    date_str: str,
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from datetime import date
    from app.entries import complete_virtual_default
    try:
        day = date.fromisoformat(date_str)
    except ValueError:
        return RedirectResponse("/", status_code=302)
    complete_virtual_default(db, day=day, content=content.strip(), current_user=current_user)
    return RedirectResponse(f"/day/{date_str}", status_code=302)


# ---------------------------------------------------------------------------
# Settings routes
# ---------------------------------------------------------------------------

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from app.default_chores import get_all_default_chores
    default_chores = get_all_default_chores(db)
    return templates.TemplateResponse(request, "settings.html", {
        "current_user": current_user,
        "default_chores": default_chores,
    })


@app.post("/settings/default-chores")
async def add_default_chore_route(
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from app.default_chores import create_default_chore
    if content.strip():
        create_default_chore(db, content=content.strip())
    return RedirectResponse("/settings", status_code=302)


@app.post("/settings/default-chores/{chore_id}/delete")
async def delete_default_chore_route(
    chore_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from app.default_chores import delete_default_chore
    delete_default_chore(db, chore_id)
    return RedirectResponse("/settings", status_code=302)


@app.post("/settings/default-chores/reorder")
async def reorder_default_chores_route(
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(require_auth),
):
    from app.default_chores import reorder_default_chores
    data = await request.json()
    ids = data.get("ids", [])
    reorder_default_chores(db, [int(i) for i in ids])
    return {"ok": True}
