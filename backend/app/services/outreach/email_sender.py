import logging
from typing import Optional

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

from app.config import settings
from app.services.outreach.templates import EmailTemplates

logger = logging.getLogger(__name__)


class OutreachSender:
    def __init__(self):
        self.api_key = settings.sendgrid_api_key
        self.sender_email = settings.sender_email
        self.sender_name = settings.sender_name
        self.templates = EmailTemplates(
            sender_name=self.sender_name,
            frontend_url=settings.frontend_url,
        )
        self._client: Optional[SendGridAPIClient] = None

    @property
    def client(self) -> Optional[SendGridAPIClient]:
        if self.api_key and self._client is None:
            self._client = SendGridAPIClient(self.api_key)
        return self._client

    def is_configured(self) -> bool:
        return bool(self.api_key and self.sender_email)

    async def send_intro(self, to_email: str, client_name: Optional[str], project_title: str) -> dict:
        return await self._send(
            to_email=to_email,
            subject=self.templates.subject(project_title, "intro"),
            html=self.templates.intro(client_name, project_title),
            plain=self.templates.plain_text_intro(client_name, project_title),
        )

    async def send_follow_up(self, to_email: str, client_name: Optional[str], project_title: str) -> dict:
        return await self._send(
            to_email=to_email,
            subject=self.templates.subject(project_title, "follow_up"),
            html=self.templates.follow_up(client_name, project_title),
        )

    async def send_proposal(self, to_email: str, client_name: Optional[str], project_title: str, amount: float) -> dict:
        return await self._send(
            to_email=to_email,
            subject=self.templates.subject(project_title, "proposal"),
            html=self.templates.proposal(client_name, project_title, amount),
        )

    async def send_delivery(self, to_email: str, client_name: Optional[str], project_title: str) -> dict:
        return await self._send(
            to_email=to_email,
            subject=self.templates.subject(project_title, "delivery"),
            html=self.templates.delivery(client_name, project_title),
        )

    async def _send(self, to_email: str, subject: str, html: str, plain: Optional[str] = None) -> dict:
        if not self.is_configured():
            logger.warning("SendGrid not configured. Email NOT sent to %s.", to_email)
            return {
                "sent": False,
                "reason": "sendgrid_not_configured",
                "to": to_email,
                "subject": subject,
            }

        message = Mail(
            from_email=Email(self.sender_email, self.sender_name),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html),
        )
        if plain:
            message.add_content(Content("text/plain", plain))

        try:
            response = self.client.send(message)
            logger.info(
                "Email sent to %s | subject='%s' | status=%s",
                to_email, subject, response.status_code,
            )
            return {
                "sent": True,
                "status_code": response.status_code,
                "to": to_email,
                "subject": subject,
            }
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, e)
            return {
                "sent": False,
                "error": str(e),
                "to": to_email,
                "subject": subject,
            }
