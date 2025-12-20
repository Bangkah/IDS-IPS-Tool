from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from src.models.user import Token, User
from src.core.security import authenticate_user, create_access_token, get_current_active_user
from src.services.siem import forward_log_to_siem
import pyotp
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str
    totp: str | None = None

@router.post("/api/login", response_model=Token)
async def login_for_access_token(form: LoginRequest):
    user = authenticate_user(None, form.username, form.password)  # Replace None with your user DB
    if not user:
        logmsg = f"Failed login for user: {form.username} from login endpoint."
        forward_log_to_siem(logmsg)
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # Require TOTP
    if not form.totp:
        totp_uri = pyotp.totp.TOTP(user.totp_secret).provisioning_uri(name=user.username, issuer_name="IDS/IPS Dashboard")
        return JSONResponse(status_code=206, content={"totp_required": True, "totp_uri": totp_uri})
    totp = pyotp.TOTP(user.totp_secret)
    if not totp.verify(form.totp):
        logmsg = f"Failed TOTP for user: {form.username}"
        forward_log_to_siem(logmsg)
        raise HTTPException(status_code=401, detail="Invalid TOTP code")
    access_token = create_access_token(data={"sub": user.username})
    logmsg = f"User {user.username} logged in successfully (2FA)."
    forward_log_to_siem(logmsg)
    return {"access_token": access_token, "token_type": "bearer"}
