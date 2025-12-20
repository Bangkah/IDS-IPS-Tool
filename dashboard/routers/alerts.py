from fastapi import APIRouter, Body
from dashboard.services.slack import send_slack
from dashboard.services.telegram import send_telegram
from dashboard.services.email import send_email

router = APIRouter(prefix="/api/alert", tags=["alerts"])

@router.post("")
def alert(
    message: str = Body(...),
    slack: bool = False,
    telegram: bool = False,
    email: bool = False,
):
    if slack: send_slack(message)
    if telegram: send_telegram(message)
    if email: send_email(message)
    return {"ok": True}
