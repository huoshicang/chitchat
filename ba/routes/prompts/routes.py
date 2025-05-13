from fastapi import Request, APIRouter
from schemas import PromptsResponseData, PromptsResponse
from services import new_prompts, del_prompts, edit_prompts, get_prompts, share_prompts

router = APIRouter()


@router.post("/new", response_model=PromptsResponse,  description="增加模型")
async def newModel(request: Request, body: PromptsResponseData):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    title = body.title
    content = body.content
    share = body.share
    model = await new_prompts(authorization=authorization, title=title, content=content, share=share)
    return model

@router.get("/del", response_model=PromptsResponse, description="删除模型")
async def delChat(request: Request, prompts_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    chats = await del_prompts(authorization=authorization, prompts_id=prompts_id)
    return chats

@router.post("/edit", response_model=PromptsResponse, description="修改聊天")
async def editModel(request: Request, body: PromptsResponseData):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    prompts_id = body.id
    title = body.title
    content = body.content
    chats = await edit_prompts(authorization=authorization, title=title, content=content, prompts_id=prompts_id)
    return chats

@router.get("/model", response_model=PromptsResponse, description="修改模型")
async def Model(request: Request):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    chats = await get_prompts(authorization=authorization)
    return chats

@router.get("/share", response_model=PromptsResponse, description="分享预设")
async def sharePrompts(request: Request, prompts_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    chats = await share_prompts(authorization=authorization, prompts_id=prompts_id)
    return chats
