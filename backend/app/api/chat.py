import json
import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.rate_limit import limiter
from app.services.chatbot import ChatbotService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])
chatbot = ChatbotService()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    client_email: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


@router.post("")
@limiter.limit("30/minute")
async def chat_message(request: Request, body: ChatRequest, db: AsyncSession = Depends(get_db)):
    session_id = body.session_id or str(uuid4())
    reply = await chatbot.process_message(db, session_id, body.message, body.client_email)
    return ChatResponse(response=reply, session_id=session_id)


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    session_id = str(uuid4())

    try:
        data = await websocket.receive_text()
        initial = json.loads(data)
        if initial.get("session_id"):
            session_id = initial["session_id"]
        if initial.get("type") == "init" and initial.get("message"):
            reply = await chatbot.process_message(db, session_id, initial["message"], initial.get("client_email"))
            await websocket.send_text(json.dumps({"type": "message", "content": reply, "session_id": session_id}))
    except Exception:
        pass

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            msg_type = data.get("type", "message")

            if msg_type == "message":
                reply = await chatbot.process_message(db, session_id, data["content"], data.get("client_email"))
                await websocket.send_text(json.dumps({"type": "message", "content": reply, "session_id": session_id}))
            elif msg_type == "clear":
                from app.models.conversation import Conversation
                from sqlalchemy import select
                result = await db.execute(
                    select(Conversation).where(Conversation.session_id == session_id)
                )
                conv = result.scalar_one_or_none()
                if conv:
                    conv.messages = []
                    await db.commit()
                await websocket.send_text(json.dumps({"type": "cleared", "session_id": session_id}))
    except WebSocketDisconnect:
        logger.info("Chat WebSocket disconnected: %s", session_id)
    except Exception as e:
        logger.error("Chat WebSocket error: %s", e)
    finally:
        await db.close()
