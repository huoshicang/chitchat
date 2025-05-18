from fastapi import Request, APIRouter
from starlette import status

from schemas import ChatResponse
from services import get_chat, share_chat, del_chat, archive_chat

router = APIRouter()

@router.get("/chat", response_model=ChatResponse, description="获取聊天列表")
async def chat(request: Request):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    chats = await get_chat(authorization=authorization)
    return chats

@router.get("/new", response_model=ChatResponse)
async def new_chat(request: Request):
    # chats = await create_new_chat(authorization=request.headers.get("authorization"))
    # # return chats
    return ChatResponse(data={}, status_code=status.HTTP_200_OK, message="不启用/new/chat")

@router.get("/del", response_model=ChatResponse, description="删除聊天")
async def delChat(request: Request, chat_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    chats = await del_chat(authorization=authorization, chat_id=chat_id)
    return chats

@router.get("/share", response_model=ChatResponse, description="分享聊天")
async def shareChat(request: Request, chat_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    chats = await share_chat(authorization=authorization, chat_id=chat_id)
    return chats



@router.get("/archive", response_model=ChatResponse, description="归档聊天")
async def archiveChat(request: Request, chat_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    chats = await archive_chat(authorization=authorization, chat_id=chat_id)
    return chats
