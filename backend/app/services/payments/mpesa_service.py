import base64
import logging
from datetime import datetime
from typing import Optional

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

SAFARICOM_SANDBOX = "https://sandbox.safaricom.co.ke"
SAFARICOM_PROD = "https://api.safaricom.co.ke"


class MpesaService:
    def __init__(self):
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0

    @property
    def base_url(self) -> str:
        return SAFARICOM_SANDBOX if settings.mpesa_environment == "sandbox" else SAFARICOM_PROD

    @property
    def enabled(self) -> bool:
        return all([
            settings.mpesa_consumer_key,
            settings.mpesa_consumer_secret,
            settings.mpesa_shortcode,
            settings.mpesa_passkey,
        ])

    async def _get_access_token(self) -> Optional[str]:
        import time as time_module
        now = time_module.time()
        if self._access_token and now < self._token_expires_at:
            return self._access_token

        if not settings.mpesa_consumer_key or not settings.mpesa_consumer_secret:
            return None

        auth = base64.b64encode(
            f"{settings.mpesa_consumer_key}:{settings.mpesa_consumer_secret}".encode()
        ).decode()

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
                    headers={"Authorization": f"Basic {auth}"},
                    timeout=10,
                )
                resp.raise_for_status()
                data = resp.json()
                self._access_token = data.get("access_token")
                self._token_expires_at = now + (data.get("expires_in", 3600) - 60)
                return self._access_token
            except Exception as e:
                logger.error("M-Pesa auth failed: %s", e)
                return None

    def _generate_password(self) -> tuple[str, str]:
        import hashlib
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        raw = f"{settings.mpesa_shortcode}{settings.mpesa_passkey}{timestamp}"
        password = base64.b64encode(hashlib.sha256(raw.encode()).hexdigest().encode()).decode()
        return password, timestamp

    async def stk_push(
        self,
        phone_number: str,
        amount: float,
        account_reference: str,
        transaction_desc: str = "Design Project Payment",
    ) -> dict:
        if not self.enabled:
            return {"error": "M-Pesa is not configured. Set all MPESA_* environment variables."}

        token = await self._get_access_token()
        if not token:
            return {"error": "Failed to authenticate with M-Pesa. Check MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET."}

        password, timestamp = self._generate_password()
        callback_url = settings.mpesa_callback_url or f"{settings.frontend_url.rstrip('/')}/api/v1/webhooks/mpesa"

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                    json={
                        "BusinessShortCode": settings.mpesa_shortcode,
                        "Password": password,
                        "Timestamp": timestamp,
                        "TransactionType": "CustomerPayBillOnline",
                        "Amount": str(int(round(amount))),
                        "PartyA": phone_number,
                        "PartyB": settings.mpesa_shortcode,
                        "PhoneNumber": phone_number,
                        "CallBackURL": callback_url,
                        "AccountReference": account_reference[:12],
                        "TransactionDesc": transaction_desc[:13],
                    },
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=15,
                )
                data = resp.json()
                logger.info("M-Pesa STK Push response: %s", data)
                return {
                    "merchant_request_id": data.get("MerchantRequestID"),
                    "checkout_request_id": data.get("CheckoutRequestID"),
                    "response_code": data.get("ResponseCode"),
                    "response_description": data.get("ResponseDescription"),
                    "raw": data,
                }
            except Exception as e:
                logger.error("M-Pesa STK Push failed: %s", e)
                return {"error": f"M-Pesa STK Push failed: {e}"}
