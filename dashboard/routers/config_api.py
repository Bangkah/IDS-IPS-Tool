from fastapi import APIRouter, Form
import os, json

router = APIRouter(prefix="/api", tags=["config"])

@router.get("/config")
def get_config():
    cfg_path = os.path.abspath("config.json")
    if not os.path.exists(cfg_path):
        return {"error": "config.json not found"}
    with open(cfg_path) as f:
        return json.load(f)

@router.post("/config")
def save_config(cfg: str = Form(...)):
    cfg_path = os.path.abspath("config.json")
    try:
        data = json.loads(cfg)
        with open(cfg_path, "w") as f:
            json.dump(data, f, indent=2)
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}
