from fastapi import APIRouter, Body, Depends
from src.models.user import User
from src.services.alerting import send_slack_alert, send_telegram_alert, send_email_alert
from src.core.security import get_current_active_user

router = APIRouter()

@router.post("/api/alert")
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
