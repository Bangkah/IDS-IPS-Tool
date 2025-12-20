import os

JWT_SECRET = os.environ.get("JWT_SECRET", "CHANGE_ME")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

ALLOWED_IPS = set(
    os.environ.get("ALLOWED_IPS", "127.0.0.1,::1").split(",")
)

SIEM_ENDPOINT = os.environ.get("SIEM_ENDPOINT")
