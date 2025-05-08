from typing import List

from pydantic import BaseModel
from starlette import status

# 聊天的响应数据
class ChatResponseData(BaseModel):
    _id: int | str
    title: str
    message_id: str

# 聊天的响应
class ChatResponse(BaseModel):
    status_code: int = status.HTTP_200_OK
    data: list[dict] | None = List[ChatResponseData]
    message: str = "成功"

# 聊天的响应
class DelChat(BaseModel):
    status_code: int = status.HTTP_200_OK
    data: dict = {}
    message: str = "成功"

# 新建聊天
class NewChat(BaseModel):
    status_code: int = status.HTTP_200_OK
    data: dict = {}

class ShareChat(BaseModel):
    status_code: int = status.HTTP_200_OK
    data: dict = {}
    message: str = "成功"