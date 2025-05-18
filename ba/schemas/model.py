from typing import List

from pydantic import BaseModel
from starlette import status

# 定义子模型
class AiConfig(BaseModel):
    api_key: str
    base_url: str

class ModelConfig(BaseModel):
    model: str
    temperature: float
    top_p: float


# 主请求体模型
class MoldeResponseData(BaseModel):
    id: str = ""
    name: str
    model_var: ModelConfig
    ai_var: AiConfig
    extra: List[dict]

# 聊天的响应
class MoldeResponse(BaseModel):
    status_code: int = status.HTTP_200_OK
    data: list[dict] | None | dict = List[MoldeResponseData]
    message: str = "成功"
