from typing import List

from pydantic import BaseModel
from starlette import status


# 发送消息内容
class SendText(BaseModel):
    role: str
    content: str

class AiConfig(BaseModel):
    # apikey
    api_key: str
    # 模型
    model: str
    base_url: str
    # 流式返回
    stream: bool = True
    # 流式返回选项
    stream_options: dict[str, bool] = {"include_usage": True}
    # 模型采样
    temperature: float = 0.4
    # 模型采样
    top_p: float = 1


# 新建消息
class NewMessage(BaseModel):
    message_id: str
    send_text: List[SendText]
    ai_var: AiConfig


# 聊天的响应
class MessageResponse(BaseModel):
    status_code: int = status.HTTP_200_OK
    data: list[dict] | None | dict = List[SendText]
    message: str = "成功"
