
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
def get_stats():
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
def get_attack_types():
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
def get_top_ips():
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
def get_status():
    # TODO: Integrasi dengan proses IDS/IPS nyata
    return {"sniffer": "Aktif", "ips": "Aktif"}

# API: Unblock IP (dummy, hanya log, harus autentikasi di produksi!)
@app.post("/api/unblock_ip")
def unblock_ip(ip: str = Form(...)):
    # TODO: Integrasi dengan iptables/unblock nyata
    print(f"[DASHBOARD] Unblock IP: {ip}")
    return {"ok": True, "msg": f"IP {ip} di-unblock (dummy)"}

# API: Get config.json
@app.get("/api/config")
def get_config():
    cfg_path = os.path.abspath("config.json")
    if not os.path.exists(cfg_path):
        return JSONResponse(status_code=404, content={"error": "config.json not found"})
    with open(cfg_path) as f:
        return json.load(f)

# API: Save config.json
@app.post("/api/config")
def save_config(cfg: str = Form(...)):
    cfg_path = os.path.abspath("config.json")
    try:
        data = json.loads(cfg)
        with open(cfg_path, "w") as f:
            json.dump(data, f, indent=2)
        return {"ok": True}
    except Exception as e:
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
