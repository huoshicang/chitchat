from fastapi import Request, APIRouter
from schemas import SettingsResponseData, SettingsResponse
from services import edit_setting

router = APIRouter()

@router.post("/edit", response_model=SettingsResponse, description="修改聊天")
async def editModel(request: Request, body: SettingsResponseData):
    authorization = request.headers.get("authorization").replace("Bearer ", "")


    _id = body.id
    setting = body.setting
    messageConfig = body.messageConfig
    siderContent = body.siderContent
    settings = await edit_setting(authorization=authorization, _id=_id, setting=setting, messageConfig=messageConfig, siderContent=siderContent)
    return settings
