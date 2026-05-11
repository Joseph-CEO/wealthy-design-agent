import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.project import Project, ProjectStatus

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/projects", tags=["Projects"])


class ProjectCreate(BaseModel):
    lead_id: int | None = None
    title: str
    description: str | None = None
    quote_amount: float | None = None
    currency: str = "USD"
    client_email: str | None = None
    deadline: str | None = None


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    quote_amount: float | None = None
    currency: str | None = None
    client_email: str | None = None
    deadline: str | None = None


@router.get("")
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    projects = result.scalars().all()
    return [_project_to_dict(p) for p in projects]


@router.post("")
async def create_project(body: ProjectCreate, db: AsyncSession = Depends(get_db)):
    deadline = None
    if body.deadline:
        try:
            deadline = datetime.fromisoformat(body.deadline)
        except ValueError:
            pass

    project = Project(
        lead_id=body.lead_id,
        title=body.title,
        description=body.description,
        quote_amount=body.quote_amount,
        currency=body.currency or "USD",
        client_email=body.client_email,
        deadline=deadline,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return _project_to_dict(project)


@router.get("/{project_id}")
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return _project_to_dict(project)


@router.put("/{project_id}")
async def update_project(project_id: int, body: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if body.title is not None:
        project.title = body.title
    if body.description is not None:
        project.description = body.description
    if body.status is not None:
        try:
            project.status = ProjectStatus(body.status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {body.status}")
    if body.quote_amount is not None:
        project.quote_amount = body.quote_amount
    if body.currency is not None:
        project.currency = body.currency
    if body.client_email is not None:
        project.client_email = body.client_email
    if body.deadline is not None:
        try:
            project.deadline = datetime.fromisoformat(body.deadline)
        except ValueError:
            pass

    project.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(project)
    return _project_to_dict(project)


def _project_to_dict(p: Project) -> dict:
    return {
        "id": p.id,
        "lead_id": p.lead_id,
        "title": p.title,
        "description": p.description,
        "status": p.status.value,
        "quote_amount": p.quote_amount,
        "currency": p.currency,
        "client_email": p.client_email,
        "started_at": p.started_at.isoformat() if p.started_at else None,
        "deadline": p.deadline.isoformat() if p.deadline else None,
        "delivered_at": p.delivered_at.isoformat() if p.delivered_at else None,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }
