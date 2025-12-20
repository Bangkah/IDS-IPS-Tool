from fastapi import APIRouter, Depends
from dashboard.core.security import authenticate
import os, json, datetime
from collections import Counter, defaultdict

router = APIRouter(prefix="/api", tags=["stats"])

@router.get("/signatures")
def get_signatures():
    cfg_path = os.path.abspath("config.json")
    if not os.path.exists(cfg_path):
        return []
    with open(cfg_path) as f:
        cfg = json.load(f)
    return cfg.get("patterns", [])
from fastapi import APIRouter, Depends
from dashboard.core.security import authenticate
import os, json, datetime
from collections import Counter, defaultdict

router = APIRouter(prefix="/api", tags=["stats"])

@router.get("/stats")
def get_stats():
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

@router.get("/attack_types")
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

@router.get("/top_ips")
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
