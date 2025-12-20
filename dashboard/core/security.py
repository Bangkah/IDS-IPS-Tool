import pyotp
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .config import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "socadmin": {
        "username": "socadmin",
        "password": "socpassword",  # plain, only for demo/dev
        "totp_secret": pyotp.random_base32(),
        "disabled": False,
    }
}

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def authenticate(username, password):
    user = fake_users_db.get(username)
    if not user:
        return None
    # Hash password at runtime for demo/dev only
    hashed = pwd_context.hash(user["password"])
    if not verify_password(password, hashed):
        return None
    return user

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
