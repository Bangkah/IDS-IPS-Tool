from fastapi import FastAPI
from dashboard.core.logging import setup_logging
from dashboard.core.middleware import IPAllowlistMiddleware, SecureHeadersMiddleware
from dashboard.core.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from dashboard.routers import auth, alerts, stats, config_api, system, ml
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

setup_logging()

app = FastAPI(title="IDS/IPS Dashboard")
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.add_middleware(IPAllowlistMiddleware)
app.add_middleware(SecureHeadersMiddleware)

app.include_router(auth.router)
app.include_router(alerts.router)
app.include_router(stats.router)
app.include_router(config_api.router)
app.include_router(system.router)
app.include_router(ml.router)

# Static & templates
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

from fastapi import Request
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
