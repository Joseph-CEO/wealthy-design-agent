import logging
import os
import shutil
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.database import init_db
from app.rate_limit import limiter
from app.scheduler import start_scheduler, stop_scheduler
from app.api.router import router
from app.api.leads import router as leads_router
from app.api.chat import router as chat_router
from app.api.payments import router as payments_router
from app.api.projects import router as projects_router
from app.api.portfolio import router as portfolio_router
from app.api.webhooks import router as webhooks_router
from app.api.admin import router as admin_router
from app.api.seo import router as seo_router

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s...", settings.app_name)
    if os.environ.get("VERCEL"):
        tmp_db = "/tmp/designer_agent.db"
        if not os.path.exists(tmp_db):
            src = os.path.join(os.path.dirname(__file__), "..", "designer_agent.db")
            if os.path.exists(src):
                shutil.copy2(src, tmp_db)
                logger.info("Copied DB to /tmp for Vercel")
    await init_db()
    logger.info("Database initialized.")
    if not os.environ.get("VERCEL"):
        start_scheduler()
    yield
    if not os.environ.get("VERCEL"):
        stop_scheduler()
    logger.info("%s shut down.", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "https://frontend-iota-rust-82.vercel.app",
        "https://wealthboxagency.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Stripe-Signature"],
)

# ── Routers ────────────────────────────────────────────
app.include_router(router, prefix="/api/v1")
app.include_router(leads_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(portfolio_router, prefix="/api/v1")
app.include_router(webhooks_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(seo_router, prefix="/api/v1")
