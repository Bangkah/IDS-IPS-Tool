
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.middleware.ip_allowlist import IPAllowlistMiddleware
from src.middleware.secure_headers import SecureHeadersMiddleware
from src.middleware.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi import _rate_limit_exceeded_handler
from src.api.dashboard import router as dashboard_router
from src.api.alert import router as alert_router
from src.api.auth import router as auth_router

app = FastAPI()

# Middleware registration
app.add_middleware(IPAllowlistMiddleware)
app.add_middleware(SecureHeadersMiddleware)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="change_this_secret")

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Routers
app.include_router(dashboard_router)
app.include_router(alert_router)
app.include_router(auth_router)
