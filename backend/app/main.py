import sys
from pathlib import Path

# Allow importing the shared mcp_connectors package from the project root
# without needing it installed as a separate pip package in local dev.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.routers import (
    dashboard,
    knowledge_graph,
    dependency_graph,
    projects,
    decisions,
    experts,
    risks,
    releases,
    analytics,
    chat,
    integrations,
    timeline,
    auth,
)
from app.routers.chat import limiter

app = FastAPI(
    title="OrgPulse AI API",
    description="Organizational Intelligence Graph backend: organizational memory, "
                 "dependency graph reasoning, predictive risk, and MCP integrations.",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Never leak internal exception details (stack traces, file paths) to
    # the client; log server-side only.
    import logging
    logging.getLogger("orgpulse").exception("Unhandled error on %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if settings.ENV != "development" and settings.JWT_SECRET == "dev-secret-change-me":
    import logging
    logging.getLogger("orgpulse").warning(
        "JWT_SECRET is set to the default dev value while ENV=%s. Set a real "
        "secret via the JWT_SECRET environment variable before deploying.",
        settings.ENV,
    )

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(knowledge_graph.router)
app.include_router(dependency_graph.router)
app.include_router(projects.router)
app.include_router(decisions.router)
app.include_router(experts.router)
app.include_router(risks.router)
app.include_router(releases.router)
app.include_router(analytics.router)
app.include_router(chat.router)
app.include_router(integrations.router)
app.include_router(timeline.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/")
def root():
    return {
        "message": "OrgPulse AI API",
        "docs": "/docs",
        "health": "/api/health",
    }
