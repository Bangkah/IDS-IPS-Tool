from fastapi import APIRouter, Depends, Request, WebSocket, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.models.user import User
from src.core.security import get_current_active_user
from src.services.siem import forward_log_to_siem
import os, json, datetime, asyncio
from collections import Counter, defaultdict

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/api/signatures")
async def get_signatures(current_user: User = Depends(get_current_active_user)):
    cfg_path = os.path.abspath("config.json")
    if not os.path.exists(cfg_path):
        return []
    with open(cfg_path) as f:
        cfg = json.load(f)
    return cfg.get("patterns", [])

@router.get("/api/stats")
async def get_stats(current_user: User = Depends(get_current_active_user)):
    log_path = os.path.abspath("ids_ips.log")
    if not os.path.exists(log_path):
        return {"labels": [], "data": []}
    per_hour = defaultdict(int)
    with open(log_path) as f:
        for line in f:
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

@router.get("/api/attack_types")
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

@router.get("/api/top_ips")
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

@router.get("/api/status")
async def get_status(current_user: User = Depends(get_current_active_user)):
    return {"sniffer": "Aktif", "ips": "Aktif"}

@router.post("/api/unblock_ip")
async def unblock_ip(ip: str = Form(...), current_user: User = Depends(get_current_active_user)):
    logmsg = f"User {current_user.username} requested unblock for IP: {ip}"
    forward_log_to_siem(logmsg)
    return {"ok": True, "msg": f"IP {ip} di-unblock (dummy)"}

@router.get("/api/config")
async def get_config(current_user: User = Depends(get_current_active_user)):
    cfg_path = os.path.abspath("config.json")
    if not os.path.exists(cfg_path):
        return JSONResponse(status_code=404, content={"error": "config.json not found"})
    with open(cfg_path) as f:
        return json.load(f)

@router.post("/api/config")
async def save_config(cfg: str = Form(...), current_user: User = Depends(get_current_active_user)):
    cfg_path = os.path.abspath("config.json")
    try:
        data = json.loads(cfg)
        with open(cfg_path, "w") as f:
            json.dump(data, f, indent=2)
        return {"ok": True}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    log_path = os.path.abspath("ids_ips.log")
    if not os.path.exists(log_path):
        open(log_path, "a").close()
    with open(log_path, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                await websocket.send_text(line.strip())
            else:
                await asyncio.sleep(1)
