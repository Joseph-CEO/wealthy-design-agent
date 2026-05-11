import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
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
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s...", settings.app_name)
    await init_db()
    logger.info("Database initialized.")
    start_scheduler()
    yield
    stop_scheduler()
    logger.info("%s shut down.", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "https://localhost:3000",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
