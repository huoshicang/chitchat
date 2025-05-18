from typing import List

from pydantic import BaseModel
from starlette import status

# 主请求体模型
class PromptsResponseData(BaseModel):
    id: str = ""
    title: str
    prompt: str
    share: bool = False


# 聊天的响应
class PromptsResponse(BaseModel):
    status_code: int = status.HTTP_200_OK
    data: list[dict] | None | dict = List[PromptsResponseData]
    message: str = "成功"
