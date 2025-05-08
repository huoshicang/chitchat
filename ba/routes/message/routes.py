from fastapi import Request, APIRouter
import httpx

from schemas import ChatResponse
from services import get_chat
from services.message.get_message import get_messages
from utils.auth import logger

router = APIRouter()


@router.get("/{message_id}", response_model=ChatResponse)
async def message(request: Request, message_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    messages = await get_messages(authorization=authorization, message_id=message_id)
    return messages

