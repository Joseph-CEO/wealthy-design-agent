import json
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.payment import Payment, PaymentGateway, PaymentStatus
from app.models.project import Project, ProjectStatus
from app.services.payments.pesapal_service import PesapalService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/pesapal")
async def pesapal_ipn(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        body = await request.json()
    except Exception:
        body = {}

    order_tracking_id = body.get("OrderTrackingId")
    merchant_reference = body.get("OrderMerchantReference")
    notification_type = body.get("OrderNotificationType")

    logger.debug("PesaPal IPN: tracking=%s ref=%s type=%s", order_tracking_id, merchant_reference, notification_type)

    if not order_tracking_id:
        return {"status": 200}

    pesapal = PesapalService()
    status_data = await pesapal.get_transaction_status(order_tracking_id)

    if "error" in status_data:
        logger.error("PesaPal IPN status check failed for %s", order_tracking_id)
        return {"status": 500}

    status_code = status_data.get("status_code")
    status_description = status_data.get("payment_status_description", "").upper()

    result = await db.execute(
        select(Payment).where(
            Payment.gateway == PaymentGateway.pesapal,
            Payment.gateway_payment_id == order_tracking_id,
        )
    )
    payment = result.scalar_one_or_none()

    if not payment:
        logger.warning("PesaPal IPN for unknown payment: %s", order_tracking_id)
        return {"status": 200}

    if status_code == 1 or status_description == "COMPLETED":
        payment.status = PaymentStatus.completed
        payment.gateway_status = "completed"
        payment.paid_at = datetime.now(timezone.utc)
        payment.receipt_url = status_data.get("confirmation_code", "")

        project = await db.get(Project, payment.project_id)
        if project:
            project.status = ProjectStatus.paid
    elif status_code == 2 or status_description == "FAILED":
        payment.status = PaymentStatus.failed
        payment.gateway_status = f"failed: {status_data.get('description', '')}"
    elif status_description == "REVERSED":
        payment.status = PaymentStatus.refunded
        payment.gateway_status = "reversed"
    else:
        payment.gateway_status = status_description

    await db.commit()
    logger.info("PesaPal payment updated: %s -> %s", order_tracking_id, payment.status.value)

    return {"status": 200}


@router.post("/mpesa")
async def mpesa_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        body = await request.json()
    except Exception:
        body = {}

    stk_callback = body.get("Body", {}).get("stkCallback", {})
    checkout_request_id = stk_callback.get("CheckoutRequestID")
    logger.debug("M-Pesa callback for checkout: %s", checkout_request_id)
    result_code = stk_callback.get("ResultCode")
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
