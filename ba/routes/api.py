from fastapi import APIRouter

from .chat import chat_router
from .message import message_router

api_router = APIRouter()

api_router.include_router(chat_router, prefix="/chats", tags=["chats"])

api_router.include_router(message_router, prefix="/messages", tags=["messages"])

