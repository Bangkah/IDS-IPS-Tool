from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from fastapi.responses import PlainTextResponse
import logging

ALLOWED_IPS = {"127.0.0.1", "::1"}  # Add your trusted IPs here

class IPAllowlistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        client_ip = request.client.host
        if client_ip not in ALLOWED_IPS:
            logging.warning(f"Blocked request from non-allowed IP: {client_ip}")
            return PlainTextResponse("Forbidden: IP not allowed", status_code=403)
        return await call_next(request)
