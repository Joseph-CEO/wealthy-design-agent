import json
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.payment import Payment, PaymentGateway, PaymentStatus
from app.models.project import Project, ProjectStatus
from app.services.payments.stripe_service import StripeService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/stripe")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    stripe = StripeService()
    event = await stripe.verify_webhook(payload, sig_header)

    if event is None and stripe.enabled:
        raise HTTPException(status_code=400, detail="Webhook verification failed")

    event_type = event["type"] if event else "checkout.session.completed"

    if event_type == "checkout.session.completed":
        session = event["data"]["object"] if event else json.loads(payload)
        session_id = session.get("id") or session.get("object", {})
        project_id = int((session.get("metadata") or {}).get("project_id", 0))
        payment_status = session.get("payment_status", "paid")

        if project_id:
            result = await db.execute(
                select(Payment).where(
                    Payment.gateway == PaymentGateway.stripe,
                    Payment.gateway_payment_id == session_id,
                )
            )
            payment = result.scalar_one_or_none()
            if payment:
                payment.status = PaymentStatus.completed if payment_status == "paid" else PaymentStatus.failed
                payment.gateway_status = payment_status
                payment.paid_at = datetime.now(timezone.utc)

                project = await db.get(Project, project_id)
                if project and payment_status == "paid":
                    project.status = ProjectStatus.paid

                await db.commit()
                logger.info("Stripe payment completed: session=%s project=%s", session_id, project_id)

    return {"status": "received"}


@router.post("/mpesa")
async def mpesa_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        body = await request.json()
    except Exception:
        body = {}

    logger.info("M-Pesa callback received: %s", json.dumps(body, default=str)[:500])

    stk_callback = body.get("Body", {}).get("stkCallback", {})
    result_code = stk_callback.get("ResultCode")
    checkout_request_id = stk_callback.get("CheckoutRequestID")
    result_desc = stk_callback.get("ResultDesc", "")

    if not checkout_request_id:
        return {"status": "received", "note": "no checkout_request_id"}

    result = await db.execute(
        select(Payment).where(
            Payment.gateway == PaymentGateway.mpesa,
            Payment.gateway_payment_id == checkout_request_id,
        )
    )
    payment = result.scalar_one_or_none()
    if not payment:
        logger.warning("M-Pesa callback for unknown payment: %s", checkout_request_id)
        return {"status": "received", "note": "unknown payment"}

    if result_code == 0:
        payment.status = PaymentStatus.completed
        payment.gateway_status = "completed"
        payment.paid_at = datetime.now(timezone.utc)

        metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
        for item in metadata:
            if item.get("Name") == "ReceiptNumber":
                payment.gateway_payment_id = item.get("Value", checkout_request_id)
                break

        project = await db.get(Project, payment.project_id)
        if project:
            project.status = ProjectStatus.paid
    else:
        payment.status = PaymentStatus.failed
        payment.gateway_status = f"failed: {result_desc}"

    await db.commit()
    logger.info("M-Pesa payment updated: %s -> %s", checkout_request_id, payment.status.value)

    return {"status": "received"}
