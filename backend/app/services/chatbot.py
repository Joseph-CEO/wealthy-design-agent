import json
import logging
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.conversation import Conversation
from app.models.portfolio import PortfolioItem

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful AI assistant for a professional graphic designer based in Nairobi, Kenya. Your role is to answer questions, provide information about services and pricing, and guide potential clients through the process of hiring the designer.

SERVICES AND PRICING (starting prices):
- Logo Design: from $150
- Book Layout & Cover Design: from $200
- Branding (full identity): from $500
- Packaging Design: from $250
- Signboard Design: from $100
- Flyer Design: from $80
- Poster Design: from $100
- Menu Design: from $120
- Banner Design: from $80
- Website Design: from $300

PROCESS:
1. Initial consultation to understand the project
2. Proposal and detailed quote
3. Design concepts (2-3 options)
4. Revisions (up to 3 rounds included)
5. Final delivery in all required formats

ABOUT THE DESIGNER:
- Based in Nairobi, Kenya
- Works with clients worldwide
- Available for remote projects
- Fast turnaround (most projects 3-7 days)
- High-quality, professional designs with attention to detail

PORTFOLIO ITEMS:
{portfolio_context}

RULES:
- When asked about pricing, always say "from $X" as a starting point and mention the final quote depends on project scope.
- When someone wants to hire, direct them to the contact page at /contact or offer to collect their email for follow-up.
- Keep responses friendly, professional, and concise.
- Do not make up specific portfolio items; only reference those listed above.
- If you don't know something, be honest and offer to connect the client with the designer directly.
- When asked about turnaround time, explain it depends on project complexity but most projects take 3-7 days.
- Always maintain a warm, helpful tone."""


def format_portfolio_for_prompt(items: list) -> str:
    if not items:
        return "No portfolio items loaded yet. Refer clients to the portfolio page at /portfolio."
    lines = []
    for item in items:
        tags_str = ", ".join(item.tags) if item.tags else ""
        lines.append(f"- {item.title} ({item.category.replace('_', ' ').title()}): {item.description or ''}{' | Tags: ' + tags_str if tags_str else ''}")
    return "\n".join(lines)


async def get_or_create_conversation(db: AsyncSession, session_id: str, client_email: Optional[str] = None) -> Conversation:
    result = await db.execute(
        select(Conversation).where(Conversation.session_id == session_id)
    )
    conv = result.scalar_one_or_none()
    if conv:
        if client_email and not conv.client_email:
            conv.client_email = client_email
        return conv
    conv = Conversation(
        session_id=session_id,
        client_email=client_email,
        messages=[],
        context={},
    )
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv


async def load_portfolio_context(db: AsyncSession) -> str:
    result = await db.execute(
        select(PortfolioItem).where(PortfolioItem.featured == True).limit(10)
    )
    items = result.scalars().all()
    return format_portfolio_for_prompt(list(items))


class ChatbotService:
    def __init__(self):
        self._openai = None

    @property
    def openai(self):
        if self._openai is None and settings.openai_api_key:
            from openai import AsyncOpenAI
            self._openai = AsyncOpenAI(api_key=settings.openai_api_key)
        return self._openai

    async def process_message(self, db: AsyncSession, session_id: str, message: str, client_email: Optional[str] = None) -> str:
        conv = await get_or_create_conversation(db, session_id, client_email)

        messages = conv.messages or []
        messages.append({"role": "user", "content": message, "timestamp": datetime.now(timezone.utc).isoformat()})

        portfolio_context = await load_portfolio_context(db)
        system_prompt = SYSTEM_PROMPT.format(portfolio_context=portfolio_context)

        if self.openai:
            try:
                chat_messages = [{"role": "system", "content": system_prompt}]
                for m in messages[-20:]:
                    chat_messages.append({"role": m["role"], "content": m["content"]})

                response = await self.openai.chat.completions.create(
                    model="gpt-4o",
                    messages=chat_messages,
                    max_tokens=500,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content.strip()
            except Exception as e:
                logger.error("OpenAI API error: %s", e)
                reply = "I'm sorry, I'm having trouble connecting to my knowledge base right now. Please try again in a moment, or send an email to the designer directly."
        else:
            reply = (
                "Thank you for your message! I'm currently operating in offline mode. "
                "Please visit the Contact page to send a direct message, and the designer will get back to you promptly."
            )

        messages.append({"role": "assistant", "content": reply, "timestamp": datetime.now(timezone.utc).isoformat()})

        conv.messages = messages
        conv.updated_at = datetime.now(timezone.utc)
        await db.commit()

        return reply
