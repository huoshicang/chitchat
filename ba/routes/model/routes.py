from fastapi import Request, APIRouter
from schemas import MoldeResponse, MoldeResponseData
from services import new_model, del_model, edit_model, get_model, share_model


router = APIRouter()


@router.post("/new", response_model=MoldeResponse,  description="增加模型")
async def newModel(request: Request, body: MoldeResponseData):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    name = body.name
    ai_var = body.ai_var
    model_var = body.model_var
    extra = body.extra
    model = await new_model(authorization=authorization, name=name, ai_var=ai_var, model_var=model_var, extra=extra)
    return model

@router.get("/del", response_model=MoldeResponse, description="删除模型")
async def delChat(request: Request, model_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    chats = await del_model(authorization=authorization, model_id=model_id)
    return chats

@router.post("/edit", response_model=MoldeResponse, description="修改聊天")
async def editModel(request: Request, body: MoldeResponseData):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    model_id = body.id
    name = body.name
    ai_var = body.ai_var
    model_var = body.model_var
    extra = body.extra
    chats = await edit_model(authorization=authorization, name=name, ai_var=ai_var, model_var=model_var, extra=extra, model_id=model_id)
    return chats

@router.get("/model", response_model=MoldeResponse, description="修改模型")
async def Model(request: Request):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    chats = await get_model(authorization=authorization)
    return chats


@router.get("/share", response_model=MoldeResponse, description="分享模型")
async def shareModel(request: Request, model_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    chats = await share_model(authorization=authorization, model_id=model_id)
    return chats
