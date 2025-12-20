import pyotp
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dashboard.core.security import authenticate, create_token, fake_users_db

router = APIRouter(prefix="/api", tags=["auth"])

class Login(BaseModel):
    username: str
    password: str
    totp: str | None = None

@router.post("/login")
def login(data: Login):
    user = authenticate(data.username, data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    totp = pyotp.TOTP(user["totp_secret"])
    if not data.totp:
        return {
            "totp_required": True,
            "uri": totp.provisioning_uri(data.username, issuer_name="IDS Dashboard"),
        }

    if not totp.verify(data.totp):
        raise HTTPException(401, "Invalid TOTP")

    token = create_token(data.username)
    logging.info(f"User {data.username} logged in")
    return {"access_token": token, "token_type": "bearer"}
