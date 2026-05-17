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
    return result
