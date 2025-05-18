import json
import time

from fastapi import FastAPI, Request, APIRouter, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette import status
from starlette.responses import JSONResponse

from config import setup_logger, get_logger
from fastapi import WebSocket

from routes import api_router
from services import send_message
from utils import judgment_auth

setup_logger()

# 获取日志记录器
logger = get_logger(__name__)

app = FastAPI(
    title="chitchat",
    description="",
    version="0.0.0",
)

api = APIRouter(prefix="/api", tags=["api"])
api.include_router(api_router)
app.include_router(api)

@app.get("/api/auth")
def root(request: Request) -> JSONResponse:
    return judgment_auth(request)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:

        data = json.loads(await websocket.receive_text())
        headers = websocket.headers
        await send_message(websocket, data, headers)
    except Exception as e:
        logger.error(f"处理websocket请求时发生错误: {e}")
        await websocket.send_text("服务器内部错误")
        await websocket.close()




# 跨域
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["localhost", '127.0.0.1'],  # 允许的源
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # 允许的方法，如 GET, POST 等
    allow_headers=["*"],  # 允许的头
)


# 定义中间件
@app.middleware("http")
@app.middleware("https")
async def process_time_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)


    if not request.headers.get("authorization", False) and request.url.path != "/auth":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "非法请求",
            },
        )

    response.headers["X-Requested-Url"] = str(request.url).replace(str(request.base_url), "")
    logger.info(f"{request.method} {request.url} {response.status_code} {time.time() - start}s")
    return response


if __name__ == '__main__':
    # 启动应用，开启热更新
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=9000,
        log_level="debug",
        reload=True)
