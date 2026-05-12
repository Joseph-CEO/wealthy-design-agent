import logging

from fastapi import APIRouter, Depends, HTTPException, Header, Query, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.config import settings
from app.models.lead import Lead, LeadStatus
from app.models.project import Project, ProjectStatus
from app.models.payment import Payment, PaymentStatus
from app.models.portfolio import PortfolioItem
from app.models.scan_log import ScanLog
from app.rate_limit import limiter
from app.services.seo_generator import generate_and_publish_pages

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["Admin"])


async def require_admin(authorization: str | None = Header(None)):
    if not settings.admin_token:
        return
    if not authorization:
        raise HTTPException(status_code=401, detail="Admin token required. Set ADMIN_TOKEN in .env or pass Authorization: Bearer <token>")
    token = authorization.replace("Bearer ", "").strip()
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Invalid admin token")


@router.get("/stats")
async def admin_stats(
    _=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    lead_total = await db.scalar(select(func.count(Lead.id)))
    lead_qualified = await db.scalar(
        select(func.count(Lead.id)).where(Lead.status == LeadStatus.qualified)
    )
    lead_converted = await db.scalar(
        select(func.count(Lead.id)).where(Lead.status == LeadStatus.converted)
    )
    lead_new = await db.scalar(
        select(func.count(Lead.id)).where(Lead.status == LeadStatus.new)
    )

    project_total = await db.scalar(select(func.count(Project.id)))
    project_active = await db.scalar(
        select(func.count(Project.id)).where(
            Project.status.in_([ProjectStatus.in_progress, ProjectStatus.review])
        )
    )
    project_delivered = await db.scalar(
        select(func.count(Project.id)).where(Project.status == ProjectStatus.delivered)
    )

    revenue_result = await db.execute(
        select(func.coalesce(func.sum(Payment.amount), 0)).where(
            Payment.status == PaymentStatus.completed
        )
    )
    total_revenue = revenue_result.scalar() or 0

    portfolio_count = await db.scalar(select(func.count(PortfolioItem.id)))

    recent_scans = await db.execute(
        select(ScanLog).order_by(ScanLog.created_at.desc()).limit(5)
    )
    scan_logs = [_scan_log_to_dict(s) for s in recent_scans.scalars().all()]

    return {
        "leads": {
            "total": lead_total or 0,
            "new": lead_new or 0,
            "qualified": lead_qualified or 0,
            "converted": lead_converted or 0,
        },
        "projects": {
            "total": project_total or 0,
            "active": project_active or 0,
            "delivered": project_delivered or 0,
        },
        "revenue": {
            "total": round(total_revenue, 2),
        },
        "portfolio_count": portfolio_count or 0,
        "recent_scans": scan_logs,
    }


@router.get("/scan-logs")
async def list_scan_logs(
    _=Depends(require_admin),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    total = await db.scalar(select(func.count(ScanLog.id)))
    result = await db.execute(
        select(ScanLog).order_by(ScanLog.created_at.desc()).offset(offset).limit(limit)
    )
    logs = result.scalars().all()
    return {
        "total": total or 0,
        "limit": limit,
        "offset": offset,
        "logs": [_scan_log_to_dict(l) for l in logs],
    }


@router.post("/generate-seo-pages")
@limiter.limit("5/minute")
async def trigger_seo_generation(
    request: Request,
    _=Depends(require_admin),
):
    """Manually trigger SEO page generation."""
    result = await generate_and_publish_pages(batch_size=settings.seo_batch_size)
    return {"status": "seo_generation_complete", **result}


def _scan_log_to_dict(log: ScanLog) -> dict:
    return {
        "id": log.id,
        "scan_type": log.scan_type,
        "status": log.status,
        "leads_found": log.leads_found,
        "message": log.message,
        "started_at": log.started_at.isoformat() if log.started_at else None,
        "completed_at": log.completed_at.isoformat() if log.completed_at else None,
        "created_at": log.created_at.isoformat() if log.created_at else None,
    }
