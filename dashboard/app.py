
# Clean entry point for modular FastAPI app
from fastapi import FastAPI

from dashboard.core.logging import setup_logging
from dashboard.core.middleware import IPAllowlistMiddleware, SecureHeadersMiddleware
from dashboard.core.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from dashboard.routers import auth, alerts, stats, config_api, system, ml

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
from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

# --- Logging Setup ---
logging.basicConfig(
    filename="dashboard_audit.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# --- Rate Limiting ---
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# --- Secure Headers Middleware ---
class SecureHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; style-src 'self' https://cdn.jsdelivr.net;"
        return response
app.add_middleware(SecureHeadersMiddleware)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import Depends, status
from pydantic import BaseModel
import secrets

# --- JWT & Auth Setup ---
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Dummy user (replace with DB/LDAP in production)
fake_users_db = {
    "socadmin": {
        "username": "socadmin",
        "full_name": "SOC Admin",
        "hashed_password": pwd_context.hash("socpassword"),
        "disabled": False,
        "totp_secret": pyotp.random_base32(),
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta=None):
    from datetime import datetime, timedelta
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# --- Alert API Endpoint ---
from fastapi import Body
@app.post("/api/alert")
async def api_alert(
    message: str = Body(...),
    slack: bool = Body(False),
    telegram: bool = Body(False),
    email: bool = Body(False),
    current_user: User = Depends(get_current_active_user)
):
    if slack:
        send_slack_alert(message)
    if telegram:
        send_telegram_alert(message)
    if email:
        send_email_alert(message)
    return {"ok": True}

# --- Security Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Uncomment for HTTPS only
# app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# --- JWT Login Endpoint ---
from slowapi.errors import RateLimitExceeded
from slowapi.decorator import limiter as rate_limit


# --- 2FA TOTP Login Endpoint ---
class LoginRequest(BaseModel):
    username: str
    password: str
    totp: str | None = None

@app.post("/api/login", response_model=Token)
@rate_limit("5/minute")
async def login_for_access_token(form: LoginRequest):
    user = authenticate_user(fake_users_db, form.username, form.password)
    if not user:
        logmsg = f"Failed login for user: {form.username} from login endpoint."
        logging.warning(logmsg)
        forward_log_to_siem(logmsg)
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # Require TOTP
    if not form.totp:
        # Provide QR code URL for first-time setup
        totp_uri = pyotp.totp.TOTP(user.totp_secret).provisioning_uri(name=user.username, issuer_name="IDS/IPS Dashboard")
        return JSONResponse(status_code=206, content={"totp_required": True, "totp_uri": totp_uri})
    totp = pyotp.TOTP(user.totp_secret)
    if not totp.verify(form.totp):
        logmsg = f"Failed TOTP for user: {form.username}"
        logging.warning(logmsg)
        forward_log_to_siem(logmsg)
        raise HTTPException(status_code=401, detail="Invalid TOTP code")
    access_token = create_access_token(data={"sub": user.username})
    logmsg = f"User {user.username} logged in successfully (2FA)."
    logging.info(logmsg)
    forward_log_to_siem(logmsg)
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import FastAPI, Request, WebSocket, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
import os
import json
from collections import Counter, defaultdict
import datetime

app = FastAPI()
templates = Jinja2Templates(directory="dashboard/templates")
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

# Endpoint signature harus setelah deklarasi app
@app.get("/api/signatures")
async def get_signatures(current_user: User = Depends(get_current_active_user)):
    cfg_path = os.path.abspath("config.json")
    if not os.path.exists(cfg_path):
        return []
    with open(cfg_path) as f:
        cfg = json.load(f)
    return cfg.get("patterns", [])

# Dashboard Web untuk IDS/IPS
# FastAPI + Jinja2 + WebSocket (rencana awal)

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
import os

from fastapi import Form, HTTPException
from fastapi.responses import JSONResponse
import json
from collections import Counter, defaultdict
import datetime


app = FastAPI()
templates = Jinja2Templates(directory="dashboard/templates")
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API: Statistik serangan per jam/hari
@app.get("/api/stats")
async def get_stats(current_user: User = Depends(get_current_active_user)):
    log_path = os.path.abspath("ids_ips.log")
    if not os.path.exists(log_path):
        return {"labels": [], "data": []}
    per_hour = defaultdict(int)
    with open(log_path) as f:
        for line in f:
            # Asumsi format: '2025-12-20 10:00:00 | ...'
            try:
                ts = line.split("|")[0].strip()
                dt = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                label = dt.strftime("%Y-%m-%d %H:00")
                per_hour[label] += 1
            except Exception:
                continue
    labels = sorted(per_hour.keys())
    data = [per_hour[l] for l in labels]
    return {"labels": labels, "data": data}

# API: Pie chart jenis serangan
@app.get("/api/attack_types")
async def get_attack_types(current_user: User = Depends(get_current_active_user)):
    log_path = os.path.abspath("ids_ips.log")
    if not os.path.exists(log_path):
        return {"labels": [], "data": []}
    types = Counter()
    with open(log_path) as f:
        for line in f:
            try:
                parts = line.split("|")
                if len(parts) > 1:
                    t = parts[1].strip()
                    types[t] += 1
            except Exception:
                continue
    labels = list(types.keys())
    data = [types[k] for k in labels]
    return {"labels": labels, "data": data}

# API: Top 5 offending IPs
@app.get("/api/top_ips")
async def get_top_ips(current_user: User = Depends(get_current_active_user)):
    log_path = os.path.abspath("ids_ips.log")
    if not os.path.exists(log_path):
        return []
    ips = Counter()
    with open(log_path) as f:
        for line in f:
            try:
                parts = line.split("|")
                if len(parts) > 3:
                    ip = parts[3].replace("IP:", "").strip()
                    ips[ip] += 1
            except Exception:
                continue
    return ips.most_common(5)

# API: Status real-time (dummy, bisa dihubungkan ke proses nyata)
@app.get("/api/status")
async def get_status(current_user: User = Depends(get_current_active_user)):
    # TODO: Integrasi dengan proses IDS/IPS nyata
    return {"sniffer": "Aktif", "ips": "Aktif"}

# API: Unblock IP (dummy, hanya log, harus autentikasi di produksi!)
@app.post("/api/unblock_ip")
@rate_limit("10/minute")
async def unblock_ip(ip: str = Form(...), current_user: User = Depends(get_current_active_user)):
    # TODO: Integrasi dengan iptables/unblock nyata
    logmsg = f"User {current_user.username} requested unblock for IP: {ip}"
    logging.info(logmsg)
    forward_log_to_siem(logmsg)
    return {"ok": True, "msg": f"IP {ip} di-unblock (dummy)"}

# API: Get config.json
@app.get("/api/config")
async def get_config(current_user: User = Depends(get_current_active_user)):
    cfg_path = os.path.abspath("config.json")
    if not os.path.exists(cfg_path):
        return JSONResponse(status_code=404, content={"error": "config.json not found"})
    with open(cfg_path) as f:
        return json.load(f)

# API: Save config.json
@app.post("/api/config")
@rate_limit("5/minute")
async def save_config(cfg: str = Form(...), current_user: User = Depends(get_current_active_user)):
    cfg_path = os.path.abspath("config.json")
    try:
        data = json.loads(cfg)
        with open(cfg_path, "w") as f:
            json.dump(data, f, indent=2)
        logmsg = f"User {current_user.username} updated config.json."
        logging.info(logmsg)
        forward_log_to_siem(logmsg)
        return {"ok": True}
    except Exception as e:
        logmsg = f"User {current_user.username} failed to update config.json: {e}"
        logging.warning(logmsg)
        forward_log_to_siem(logmsg)
        return JSONResponse(status_code=400, content={"error": str(e)})

# WebSocket untuk live feed notifikasi nyata dari file log
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    log_path = os.path.abspath("ids_ips.log")
    # Jika file belum ada, buat kosong
    if not os.path.exists(log_path):
        open(log_path, "a").close()
    with open(log_path, "r") as f:
        # Mulai dari akhir file (hanya baris baru)
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                await websocket.send_text(line.strip())
            else:
                await asyncio.sleep(1)

if __name__ == "__main__":
    uvicorn.run("dashboard.app:app", host="0.0.0.0", port=8000, reload=True)
