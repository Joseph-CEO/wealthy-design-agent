import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)


class StripeService:
    def __init__(self):
        self._stripe = None

    @property
    def stripe(self):
        if self._stripe is None and settings.stripe_secret_key:
            import stripe
            stripe.api_key = settings.stripe_secret_key
            self._stripe = stripe
        return self._stripe

    @property
    def enabled(self) -> bool:
        return self.stripe is not None and bool(settings.stripe_publishable_key)

    async def create_checkout_session(
        self,
        project_id: int,
        amount: float,
        currency: str = "usd",
        client_email: Optional[str] = None,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
    ) -> dict:
        if not self.enabled:
            return {"error": "Payment service is not configured"}

        base_url = settings.frontend_url.rstrip("/")
        session = self.stripe.checkout.Session.create(
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": currency.lower(),
                    "product_data": {
                        "name": f"Design Project #{project_id}",
                    },
                    "unit_amount": int(round(amount * 100)),
                },
                "quantity": 1,
            }],
            client_reference_id=str(project_id),
            customer_email=client_email,
            success_url=success_url or f"{base_url}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=cancel_url or f"{base_url}/payment/cancel",
            metadata={"project_id": str(project_id)},
        )

        return {
            "session_id": session.id,
            "url": session.url,
            "publishable_key": settings.stripe_publishable_key,
        }

    async def verify_webhook(self, payload: bytes, sig_header: str) -> Optional[dict]:
        if not self.stripe or not settings.stripe_webhook_secret:
            return None

        try:
            event = self.stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
            return event
        except Exception as e:
            logger.error("Stripe webhook verification failed: %s", e)
            return None

    def get_publishable_key(self) -> Optional[str]:
        return settings.stripe_publishable_key
