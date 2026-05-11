import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.project import Project
from app.models.payment import Payment, PaymentGateway, PaymentStatus
from app.services.payments.stripe_service import StripeService
from app.services.payments.mpesa_service import MpesaService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/payments", tags=["Payments"])


class CheckoutRequest(BaseModel):
    project_id: int
    success_url: str | None = None
    cancel_url: str | None = None


class MpesaRequest(BaseModel):
    project_id: int
    phone_number: str
    amount: float | None = None


@router.post("/create-checkout-session")
async def create_checkout_session(body: CheckoutRequest, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, body.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not project.quote_amount or project.quote_amount <= 0:
        raise HTTPException(status_code=400, detail="Project has no quote amount set")

    stripe = StripeService()
    result = await stripe.create_checkout_session(
        project_id=project.id,
        amount=project.quote_amount,
        currency=project.currency,
        client_email=project.client_email,
        success_url=body.success_url,
        cancel_url=body.cancel_url,
    )

    if "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])

    payment = Payment(
        project_id=project.id,
        amount=project.quote_amount,
        currency=project.currency,
        gateway=PaymentGateway.stripe,
        gateway_payment_id=result["session_id"],
        gateway_status="pending",
        status=PaymentStatus.pending,
        client_email=project.client_email,
    )
    db.add(payment)
    await db.commit()

    return result


@router.post("/mpesa-stk-push")
async def mpesa_stk_push(body: MpesaRequest, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, body.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    amount = body.amount or project.quote_amount
    if not amount or amount <= 0:
        raise HTTPException(status_code=400, detail="No amount specified and project has no quote")

    mpesa = MpesaService()
    if not mpesa.enabled:
        raise HTTPException(status_code=503, detail="M-Pesa is not configured")

    phone = body.phone_number.strip()
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+"):
        phone = phone[1:]
    if not phone.startswith("254") or len(phone) != 12:
        raise HTTPException(status_code=400, detail="Invalid phone number. Use format: 0712345678 or +254712345678")

    result = await mpesa.stk_push(
        phone_number=phone,
        amount=amount,
        account_reference=f"PROJ-{project.id}",
    )

    if "error" in result:
        raise HTTPException(status_code=502, detail=result["error"])

    payment = Payment(
        project_id=project.id,
        amount=amount,
        currency="KES",
        gateway=PaymentGateway.mpesa,
        gateway_payment_id=result.get("checkout_request_id"),
        gateway_status=result.get("response_code"),
        status=PaymentStatus.pending,
        client_email=project.client_email,
    )
    db.add(payment)
    await db.commit()

    return result
