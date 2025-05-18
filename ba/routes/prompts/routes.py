from fastapi import Request, APIRouter
from schemas import PromptsResponseData, PromptsResponse
from services import new_prompts, del_prompts, edit_prompts, get_prompts, share_prompts

router = APIRouter()

@router.get("/porompts", response_model=PromptsResponse, description="获取提示")
async def Prompts(request: Request):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    porompts = await get_prompts(authorization=authorization)
    return porompts

@router.post("/new", response_model=PromptsResponse,  description="增加提示")
async def newPrompts(request: Request, body: PromptsResponseData):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    title = body.title
    prompt = body.prompt
    porompts = await new_prompts(authorization=authorization, title=title, prompt=prompt)
    return porompts

@router.get("/del", response_model=PromptsResponse, description="删除提示")
async def delPrompts(request: Request, prompts_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    porompts = await del_prompts(authorization=authorization, prompts_id=prompts_id)
    return porompts

@router.post("/edit", response_model=PromptsResponse, description="修改提示")
async def editPrompts(request: Request, body: PromptsResponseData):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    prompts_id = body.id
    title = body.title
    prompt = body.prompt
    porompts = await edit_prompts(authorization=authorization, title=title, prompt=prompt, prompts_id=prompts_id)
    return porompts

@router.get("/share", response_model=PromptsResponse, description="分享提示")
async def sharePrompts(request: Request, prompts_id: str):
    authorization = request.headers.get("authorization").replace("Bearer ", "")
    porompts = await share_prompts(authorization=authorization, prompts_id=prompts_id)
    return porompts
