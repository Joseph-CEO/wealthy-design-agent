import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.lead import Lead, LeadStatus
from app.services.qualification import qualify_lead
from app.services.discovery.orchestrator import DiscoveryOrchestrator
from app.services.outreach import OutreachSender

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("")
async def list_leads(
    status: Optional[LeadStatus] = Query(None),
    source: Optional[str] = Query(None),
    min_score: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    base = select(Lead)
    if status:
        base = base.where(Lead.status == status)
    if source:
        base = base.where(Lead.source == source)
    if min_score is not None:
        base = base.where(Lead.score >= min_score)

    total = await db.scalar(select(func.count()).select_from(base.subquery()))

    query = base.order_by(Lead.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    leads = result.scalars().all()

    return {
        "total": total or 0,
        "limit": limit,
        "offset": offset,
        "leads": [_lead_to_dict(l) for l in leads],
    }


@router.get("/{lead_id}")
async def get_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    lead = await db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return _lead_to_dict(lead)


@router.delete("/{lead_id}")
async def delete_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    lead = await db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    await db.delete(lead)
    await db.commit()
    return {"status": "deleted", "id": lead_id}


@router.post("/{lead_id}/qualify")
async def qualify_lead_endpoint(lead_id: int, db: AsyncSession = Depends(get_db)):
    lead = await db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    score, decision = await qualify_lead(lead)
    lead.score = score
    lead.status = LeadStatus(decision)
    await db.commit()

    return {
        "id": lead.id,
        "score": score,
        "status": lead.status.value,
        "decision": decision,
    }


@router.post("/{lead_id}/contact")
async def contact_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    """Send intro email and mark lead as contacted."""
    lead = await db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if lead.status == LeadStatus.contacted:
        return {"status": "already_contacted", "id": lead_id}

    if not lead.client_email:
        raise HTTPException(status_code=400, detail="Lead has no email address")

    sender = OutreachSender()
    result = await sender.send_intro(
        to_email=lead.client_email,
        client_name=lead.client_name,
        project_title=lead.title,
    )

    lead.status = LeadStatus.contacted
    await db.commit()

    return {
        "status": "contacted",
        "id": lead_id,
        "email": result,
    }


@router.post("/scan")
async def trigger_scan(db: AsyncSession = Depends(get_db)):
    """Manually trigger a discovery scan."""
    orchestrator = DiscoveryOrchestrator(db)
    summary = await orchestrator.run_full_scan()
    return {"status": "scan_complete", "summary": summary}


@router.post("/qualify-all")
async def qualify_all_new_leads(db: AsyncSession = Depends(get_db)):
    """Run qualification on all new/unscored leads."""
    result = await db.execute(
        select(Lead).where(Lead.status == LeadStatus.new)
    )
    leads = result.scalars().all()
    results = []
    for lead in leads:
        score, decision = await qualify_lead(lead)
        lead.score = score
        lead.status = LeadStatus(decision)
        results.append({"id": lead.id, "score": score, "status": decision})
    await db.commit()
    return {"qualified": len(results), "results": results}


@router.post("/outreach-qualified")
async def outreach_qualified_leads(db: AsyncSession = Depends(get_db)):
    """Send intro emails to all qualified leads that haven't been contacted yet."""
    result = await db.execute(
        select(Lead).where(
            Lead.status == LeadStatus.qualified,
            Lead.client_email.isnot(None),
        )
    )
    leads = result.scalars().all()
    sender = OutreachSender()
    results = []
    for lead in leads:
        email_result = await sender.send_intro(
            to_email=lead.client_email,
            client_name=lead.client_name,
            project_title=lead.title,
        )
        if email_result.get("sent"):
            lead.status = LeadStatus.contacted
        results.append({
            "id": lead.id,
            "title": lead.title,
            "email_sent": email_result.get("sent", False),
        })
    await db.commit()
    return {"total": len(results), "results": results}


@router.post("/outreach-followup")
async def send_follow_ups(db: AsyncSession = Depends(get_db)):
    """Send follow-up emails to contacted leads (3+ days since contact)."""
    from datetime import datetime, timedelta, timezone

    cutoff = datetime.now(timezone.utc) - timedelta(days=3)
    result = await db.execute(
        select(Lead).where(
            Lead.status == LeadStatus.contacted,
            Lead.updated_at <= cutoff,
            Lead.client_email.isnot(None),
        )
    )
    leads = result.scalars().all()
    sender = OutreachSender()
    results = []
    for lead in leads:
        email_result = await sender.send_follow_up(
            to_email=lead.client_email,
            client_name=lead.client_name,
            project_title=lead.title,
        )
        results.append({
            "id": lead.id,
            "title": lead.title,
            "email_sent": email_result.get("sent", False),
        })
    return {"total": len(results), "results": results}


def _lead_to_dict(lead: Lead) -> dict:
    return {
        "id": lead.id,
        "source": lead.source,
        "title": lead.title,
        "description": lead.description,
        "client_name": lead.client_name,
        "client_email": lead.client_email,
        "budget_min": lead.budget_min,
        "budget_max": lead.budget_max,
        "currency": lead.currency,
        "location": lead.location,
        "service_type": lead.service_type.value if lead.service_type else None,
        "score": lead.score,
        "status": lead.status.value,
        "created_at": lead.created_at.isoformat() if lead.created_at else None,
        "updated_at": lead.updated_at.isoformat() if lead.updated_at else None,
    }
