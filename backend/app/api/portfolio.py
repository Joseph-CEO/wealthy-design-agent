import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.portfolio import PortfolioItem, PortfolioCategory

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


class PortfolioCreate(BaseModel):
    title: str
    description: str | None = None
    category: str
    image_urls: list[str] = []
    project_url: str | None = None
    tags: list[str] = []
    featured: bool = False


class PortfolioUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    image_urls: list[str] | None = None
    project_url: str | None = None
    tags: list[str] | None = None
    featured: bool | None = None


@router.get("")
async def list_portfolio(
    category: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    base = select(PortfolioItem)
    if category:
        try:
            cat_enum = PortfolioCategory(category)
            base = base.where(PortfolioItem.category == cat_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    if featured is not None:
        base = base.where(PortfolioItem.featured == featured)

    from sqlalchemy import func
    total = await db.scalar(select(func.count()).select_from(base.subquery()))

    result = await db.execute(base.order_by(PortfolioItem.created_at.desc()).offset(offset).limit(limit))
    items = result.scalars().all()

    return {
        "total": total or 0,
        "limit": limit,
        "offset": offset,
        "items": [_item_to_dict(i) for i in items],
    }


@router.post("")
async def create_portfolio_item(body: PortfolioCreate, db: AsyncSession = Depends(get_db)):
    try:
        category = PortfolioCategory(body.category)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid category: {body.category}. Must be one of: {[c.value for c in PortfolioCategory]}")

    item = PortfolioItem(
        title=body.title,
        description=body.description,
        category=category,
        image_urls=body.image_urls or [],
        project_url=body.project_url,
        tags=body.tags or [],
        featured=body.featured,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return _item_to_dict(item)


@router.put("/{item_id}")
async def update_portfolio_item(item_id: int, body: PortfolioUpdate, db: AsyncSession = Depends(get_db)):
    item = await db.get(PortfolioItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")

    if body.title is not None:
        item.title = body.title
    if body.description is not None:
        item.description = body.description
    if body.category is not None:
        try:
            item.category = PortfolioCategory(body.category)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {body.category}")
    if body.image_urls is not None:
        item.image_urls = body.image_urls
    if body.project_url is not None:
        item.project_url = body.project_url
    if body.tags is not None:
        item.tags = body.tags
    if body.featured is not None:
        item.featured = body.featured

    item.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(item)
    return _item_to_dict(item)


@router.delete("/{item_id}")
async def delete_portfolio_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(PortfolioItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    await db.delete(item)
    await db.commit()
    return {"status": "deleted", "id": item_id}


def _item_to_dict(item: PortfolioItem) -> dict:
    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "category": item.category.value,
        "image_urls": item.image_urls or [],
        "project_url": item.project_url,
        "tags": item.tags or [],
        "featured": item.featured,
        "created_at": item.created_at.isoformat() if item.created_at else None,
        "updated_at": item.updated_at.isoformat() if item.updated_at else None,
    }
