import json
from typing import Union
from starlette import status
from fastapi import WebSocket


async def ws_send_response(websocket: WebSocket, error_message: Union[str, dict], status_code: int = status.HTTP_200_OK) -> None:
    """
    发送响应，支持字符串或字典格式。
    """
    response = {
        "status_code": status_code,
        "message": error_message
    }
    # 如果 error_message 是 dict，避免双重编码
    await websocket.send_text(json.dumps(response, ensure_ascii=False))