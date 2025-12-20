import pyotp
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .config import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "socadmin": {
        "username": "socadmin",
        "hashed_password": pwd_context.hash("socpassword"),
        "totp_secret": pyotp.random_base32(),
        "disabled": False,
    }
}

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def authenticate(username, password):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
