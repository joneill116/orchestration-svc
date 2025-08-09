
"""
FastAPI entry point for orchestration-svc.
This service exposes only orchestration APIs—no business logic, adapters, or integrations.
All dependencies are injected for testability and microservice clarity.
"""


import logging
import sys
import uuid
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from orchestration_svc.api.routes import router as api_router
from orchestration_svc.container import Container
from orchestration_svc.config import settings

# Configure structured, machine-parsable logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    stream=sys.stdout,
)
logger = logging.getLogger("orchestration_svc")

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware to propagate correlation/trace IDs for all requests.
    Adds X-Correlation-ID header if not present and logs it.
    """
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["x-correlation-id"] = correlation_id
        logger.info(f"correlation_id={correlation_id} method={request.method} path={request.url.path}")
        return response

app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(CorrelationIdMiddleware)

container = Container()
app.container = container

app.include_router(api_router, prefix=f"{settings.API_PREFIX}/v1")
