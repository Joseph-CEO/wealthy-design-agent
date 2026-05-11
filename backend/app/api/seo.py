import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.seo_page import SEOPage

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/seo", tags=["SEO"])


@router.get("/pages")
async def list_seo_pages(
    service_type: Optional[str] = Query(None),
    county: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    published: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    base = select(SEOPage)
    if service_type:
        base = base.where(SEOPage.service_type == service_type)
    if county:
        base = base.where(SEOPage.county == county)
    if industry:
        base = base.where(SEOPage.industry == industry)
    if published is not None:
        base = base.where(SEOPage.published == published)

    total = await db.scalar(select(func.count()).select_from(base.subquery()))
    result = await db.execute(
        base.order_by(SEOPage.score.desc(), SEOPage.created_at.desc())
        .offset(offset).limit(limit)
    )
    pages = result.scalars().all()

    return {
        "total": total or 0,
        "limit": limit,
        "offset": offset,
        "pages": [_page_to_dict(p) for p in pages],
    }


@router.get("/pages/{slug}")
async def get_seo_page(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SEOPage).where(SEOPage.slug == slug))
    page = result.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="SEO page not found")
    return _page_to_dict(page)


@router.get("/counties")
async def list_counties(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SEOPage.county, func.count(SEOPage.id))
        .where(SEOPage.published == True)
        .group_by(SEOPage.county)
        .order_by(func.count(SEOPage.id).desc())
    )
    return {"counties": [{"name": row[0], "page_count": row[1]} for row in result.fetchall()]}


@router.get("/services")
async def list_services(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SEOPage.service_type, func.count(SEOPage.id))
        .where(SEOPage.published == True)
        .group_by(SEOPage.service_type)
        .order_by(func.count(SEOPage.id).desc())
    )
    return {"services": [{"type": row[0], "page_count": row[1]} for row in result.fetchall()]}


def _page_to_dict(page: SEOPage) -> dict:
    return {
        "id": page.id,
        "slug": page.slug,
        "service_type": page.service_type,
        "county": page.county,
        "industry": page.industry,
        "title": page.title,
        "meta_description": page.meta_description,
        "h1": page.h1,
        "body_html": page.body_html,
        "portfolio_examples": page.portfolio_examples or [],
        "pricing_html": page.pricing_html,
        "cta_text": page.cta_text,
        "schema_json": page.schema_json,
        "score": page.score,
        "published": page.published,
        "created_at": page.created_at.isoformat() if page.created_at else None,
        "updated_at": page.updated_at.isoformat() if page.updated_at else None,
    }
