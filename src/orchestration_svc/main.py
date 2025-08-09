from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import status
from typing import Any

"""
FastAPI entry point for orchestration-svc.
This service exposes only orchestration APIs—no business logic, adapters, or integrations.
All dependencies are injected for testability and microservice clarity.
"""


import logging
import sys
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from orchestration_svc.container import Container
from orchestration_svc.api.routes import router as api_router
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


# Subclass FastAPI to add a container attribute for type safety
# Subclass FastAPI to add a container attribute for type safety
class OrchestrationApp(FastAPI):
    container: Container


# --- Extraordinary error handling ---
def error_response(status_code: int, code: str, message: str, detail: Any = None):
    body = {"error": {"code": code, "message": message}}
    if detail is not None:
        body["error"]["detail"] = detail
    return JSONResponse(status_code=status_code, content=body)

def add_global_exception_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        return error_response(
            status_code=exc.status_code,
            code=f"HTTP_{exc.status_code}",
            message=exc.detail if hasattr(exc, "detail") else str(exc),
        )

    @app.exception_handler(FastAPIRequestValidationError)
    async def validation_exception_handler(request, exc):
        return error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="VALIDATION_ERROR",
            message="Request validation failed",
            detail=exc.errors(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request, exc):
        return error_response(
            status_code=500,
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            detail=str(exc),
        )



app = OrchestrationApp(
    title=settings.PROJECT_NAME,
    description="Minimal orchestration service. All business logic, adapters, and domain models are externalized.",
    version="1.0.0",
    contact={
        "name": "orchestration-svc maintainers",
        "url": "https://github.com/joneill116/orchestration-svc",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
app.add_middleware(CorrelationIdMiddleware)

# Register global exception handlers after app is defined
add_global_exception_handlers(app)

# Allow CORS for all origins (customize as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

container = Container()
app.container = container

app.include_router(api_router, prefix=f"{settings.API_PREFIX}/v1")
