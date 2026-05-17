import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.project import Project
from app.models.payment import Payment, PaymentGateway, PaymentStatus
from app.rate_limit import limiter
from app.config import settings
from app.services.payments.pesapal_service import PesapalService
from app.services.payments.mpesa_service import MpesaService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/payments", tags=["Payments"])


class PesapalRequest(BaseModel):
    project_id: int
    client_first_name: str = ""
    client_last_name: str = ""
    client_phone: str = ""


class MpesaRequest(BaseModel):
    project_id: int
    phone_number: str
    amount: float | None = None


@router.post("/create-pesapal-order")
@limiter.limit("20/minute")
async def create_pesapal_order(request: Request, body: PesapalRequest, db: AsyncSession = Depends(get_db)):
    try:
        project = await db.get(Project, body.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if not project.quote_amount or project.quote_amount <= 0:
            raise HTTPException(status_code=400, detail="Project has no quote amount set")

        pesapal = PesapalService()
        if not pesapal.enabled:
            raise HTTPException(status_code=503, detail="PesaPal is not configured")

        ipn_id = settings.pesapal_ipn_id
        if not ipn_id:
            ipn_id = await pesapal.register_ipn(
                ipn_url="https://api-production-8de3.up.railway.app/api/v1/webhooks/pesapal"
            )
            if not ipn_id:
                raise HTTPException(status_code=503, detail="Failed to register PesaPal IPN URL")

        callback_url = f"{settings.frontend_url.rstrip('/')}/payment/success?order_tracking_id="
        result = await pesapal.submit_order(
            project_id=project.id,
            amount=project.quote_amount,
            currency=project.currency if project.currency in ("KES", "USD", "EUR", "GBP") else "KES",
            description=f"Design Project #{project.id}",
            client_email=project.client_email or "",
            client_phone=body.client_phone,
            client_first_name=body.client_first_name,
            client_last_name=body.client_last_name,
            callback_url=callback_url,
            notification_id=ipn_id,
        )

        logger.info("PesaPal submit_order result: %s", result)

        if result.get("error"):
            raise HTTPException(status_code=502, detail=result["error"])

        payment = Payment(
            project_id=project.id,
            amount=project.quote_amount,
            currency=project.currency,
            gateway=PaymentGateway.pesapal,
            gateway_payment_id=result.get("order_tracking_id"),
            gateway_status="pending",
            status=PaymentStatus.pending,
            client_email=project.client_email,
        )
        db.add(payment)
        await db.commit()

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error("PesaPal order failed: %s", e, exc_info=True)
        raise HTTPException(status_code=502, detail=str(e))


@router.post("/mpesa-stk-push")
@limiter.limit("10/minute")
async def mpesa_stk_push(request: Request, body: MpesaRequest, db: AsyncSession = Depends(get_db)):
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
