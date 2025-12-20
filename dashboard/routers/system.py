from fastapi import APIRouter, Form
from dashboard.services.siem import forward_log_to_siem

router = APIRouter(prefix="/api", tags=["system"])

@router.get("/status")
def get_status():
    return {"sniffer": "Aktif", "ips": "Aktif"}

@router.post("/unblock_ip")
def unblock_ip(ip: str = Form(...)):
    logmsg = f"User requested unblock for IP: {ip}"
    forward_log_to_siem(logmsg)
    return {"ok": True, "msg": f"IP {ip} di-unblock (dummy)"}
