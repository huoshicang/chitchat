from fastapi import APIRouter

from .chat import chat_router
from .message import message_router
from .model import model_router
from .prompts import prompts_router
from .setting import setting_router

api_router = APIRouter()

api_router.include_router(chat_router, prefix="/chats", tags=["chats"])

api_router.include_router(message_router, prefix="/messages", tags=["messages"])

api_router.include_router(model_router, prefix="/model", tags=["model"])

api_router.include_router(prompts_router, prefix="/prompts", tags=["prompts"])

api_router.include_router(setting_router, prefix="/setting", tags=["prompts"])

