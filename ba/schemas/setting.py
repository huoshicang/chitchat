from typing import List, Union

from pydantic import BaseModel
from starlette import status


# 主请求体模型
class MessageConfig(BaseModel):
    showAll : bool
    showModel: bool
    showPromptTokens: bool
    showCompletionTokens: bool
    showTotalTokens: bool
    showReasoningTokens: bool
    showTime: bool
    think: bool

# 主请求体模型
class SiderContent(BaseModel):
    display: bool
    id: bool
    share: bool
    archive: bool



# 主请求体模型
class SettingsResponseData(BaseModel):
    id: str
    setting: str
    messageConfig: MessageConfig
    siderContent: SiderContent


# 聊天的响应
class SettingsResponse(BaseModel):
    status_code: int = status.HTTP_200_OK
    data: list[dict] | None | dict = List[SettingsResponseData]
    message: str = "成功"
