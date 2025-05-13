from fastapi import Request, APIRouter
from schemas import ChatResponse
from services import get_messages

router = APIRouter()


@router.get("/{message_id}", response_model=ChatResponse)
async def message(request: Request, message_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    messages = await get_messages(authorization=authorization, message_id=message_id)
    return messages

