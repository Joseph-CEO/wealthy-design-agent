import logging

from fastapi import APIRouter

from app.services.payments.pesapal_service import PesapalService
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok", "app": "Nairobi Designer Agent"}


@router.get("/debug/pesapal")
async def debug_pesapal():
    p = PesapalService()
    result = {
        "enabled": p.enabled,
        "has_consumer_key": bool(settings.pesapal_consumer_key),
        "has_consumer_secret": bool(settings.pesapal_consumer_secret),
        "has_ipn_id": bool(settings.pesapal_ipn_id),
        "environment": settings.pesapal_environment,
    }
    if p.enabled:
        token = await p._get_token()
        result["token_obtained"] = token is not None
        result["token_prefix"] = token[:20] if token else None
        if token:
            ipn_id = settings.pesapal_ipn_id
            if not ipn_id:
                ipn_id = await p.register_ipn(
                    ipn_url="https://api-production-8de3.up.railway.app/api/v1/webhooks/pesapal"
                )
            result["ipn_id"] = ipn_id
            if ipn_id:
                order = await p.submit_order(
                    project_id=0,
                    amount=1,
                    currency="KES",
                    description="Debug Test",
                    client_email="debug@test.com",
                    client_phone="254708374149",
                    client_first_name="Debug",
                    client_last_name="Test",
                    callback_url="https://wealthboxagency.vercel.app/payment/success",
                    notification_id=ipn_id,
                )
                result["submit_order"] = {k: v for k, v in order.items() if k != "raw"}
    return result
