import json
import logging
from typing import Optional

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

PESAPAL_SANDBOX = "https://cybqa.pesapal.com/pesapalv3"
PESAPAL_PROD = "https://pay.pesapal.com/v3"


class PesapalService:
    def __init__(self):
        self._token: Optional[str] = None

    @property
    def base_url(self) -> str:
        return PESAPAL_SANDBOX if settings.pesapal_environment == "sandbox" else PESAPAL_PROD

    @property
    def enabled(self) -> bool:
        return bool(settings.pesapal_consumer_key and settings.pesapal_consumer_secret)

    async def _get_token(self) -> Optional[str]:
        if not self.enabled:
            return None

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/api/Auth/RequestToken",
                    json={
                        "consumer_key": settings.pesapal_consumer_key,
                        "consumer_secret": settings.pesapal_consumer_secret,
                    },
                    headers={"Accept": "application/json", "Content-Type": "application/json"},
                    timeout=10,
                )
                resp.raise_for_status()
                data = resp.json()
                self._token = data.get("token")
                return self._token
            except Exception as e:
                logger.error("PesaPal auth failed: %s", e)
                return None

    async def register_ipn(self, ipn_url: str, notification_type: str = "POST") -> Optional[str]:
        token = await self._get_token()
        if not token:
            return None

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/api/URLSetup/RegisterIPN",
                    json={"url": ipn_url, "ipn_notification_type": notification_type},
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}",
                    },
                    timeout=10,
                )
                resp.raise_for_status()
                data = resp.json()
                ipn_id = data.get("ipn_id")
                if ipn_id:
                    logger.info("PesaPal IPN registered: %s -> %s", ipn_id, ipn_url)
                return ipn_id
            except Exception as e:
                logger.error("PesaPal IPN registration failed: %s", e)
                return None

    async def submit_order(
        self,
        project_id: int,
        amount: float,
        currency: str = "KES",
        description: str = "Design Project Payment",
        client_email: str = "",
        client_phone: str = "",
        client_first_name: str = "",
        client_last_name: str = "",
        callback_url: str = "",
        notification_id: str = "",
    ) -> dict:
        token = await self._get_token()
        if not token:
            return {"error": "Payment service authentication failed"}

        merchant_reference = f"PROJ-{project_id}"

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/api/Transactions/SubmitOrderRequest",
                    json={
                        "id": merchant_reference,
                        "currency": currency,
                        "amount": round(amount, 2),
                        "description": description[:100],
                        "callback_url": callback_url,
                        "notification_id": notification_id,
                        "billing_address": {
                            "email_address": client_email,
                            "phone_number": client_phone,
                            "country_code": "KE",
                            "first_name": client_first_name,
                            "middle_name": "",
                            "last_name": client_last_name,
                            "line_1": "",
                            "line_2": "",
                            "city": "",
                            "state": "",
                            "postal_code": "",
                            "zip_code": "",
                        },
                    },
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}",
                    },
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()
                logger.debug("PesaPal submit order response: %s", json.dumps(data))
                return {
                    "order_tracking_id": data.get("order_tracking_id"),
                    "merchant_reference": data.get("merchant_reference"),
                    "redirect_url": data.get("redirect_url"),
                    "status": data.get("status"),
                    "error": data.get("error"),
                }
            except Exception as e:
                logger.error("PesaPal submit order failed: %s", e)
                return {"error": f"PesaPal submit order failed: {e}"}

    async def get_transaction_status(self, order_tracking_id: str) -> dict:
        token = await self._get_token()
        if not token:
            return {"error": "Payment service authentication failed"}

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{self.base_url}/api/Transactions/GetTransactionStatus",
                    params={"orderTrackingId": order_tracking_id},
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}",
                    },
                    timeout=10,
                )
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                logger.error("PesaPal get transaction status failed: %s", e)
                return {"error": f"PesaPal get transaction status failed: {e}"}
