
from fastapi import APIRouter, Body
from pydantic import BaseModel
from dashboard.services.slack import send_slack
from dashboard.services.telegram import send_telegram
from dashboard.services.email import send_email

router = APIRouter(prefix="/api/alert", tags=["alerts"])

class AlertRequest(BaseModel):
    message: str
    slack: bool = False
    telegram: bool = False
    email: bool = False

@router.post("")
def alert(req: AlertRequest):
    if req.slack:
        send_slack(req.message)
    if req.telegram:
        send_telegram(req.message)
    if req.email:
        send_email(req.message)
    return {"ok": True}
