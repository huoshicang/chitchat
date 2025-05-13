from typing import List

from fastapi import WebSocket
from pymongo.errors import PyMongoError
from bson import ObjectId
from starlette import status
from config import get_logger
from database import MongoDB
from schemas import NewMessage
from services import create_new_chat
from utils import ws_send_response, transition_message
from utils.initiate_ai import initiate_ai

logger = get_logger(__name__)


async def get_message(message_id: str, authorization: str, websocket: WebSocket, db: MongoDB, prompt: List[dict]) -> List[dict]:
    """
    获取消息数据
    :param message_id: 消息id
    :param authorization: 认证id
    :param websocket: ws
    :param db: mongdb
    :param prompt: 发送的消息
    :return:
    """
    message, error_message = db.find_one("message", {"user_id": authorization, "_id": ObjectId(message_id)},
                                         {"message": True, "_id": False})()
    if error_message != "":
        logger.error(f"获取用户 {authorization} 的聊天记录时发生错误: {error_message}")
        await ws_send_response(websocket, f"数据库错误: {error_message}", status.HTTP_400_BAD_REQUEST)
    if message:
        message = transition_message(message.get("message", []))
        message.extend(prompt)

    return message if message else prompt


async def send_message(websocket: WebSocket, message_data: NewMessage, headers) -> None:
    """
    处理 WebSocket 消息，发送消息并返回 AI 响应。
    """
    # 浏览器指纹
    authorization = headers.get("authorization", "").replace("Bearer ", "")
    message_id = message_data.get("message_id", "")
    message_index = message_data.get("message_index", 0)
    prompt = message_data.get("prompt", [])
    ai_var = message_data.get("ai_var", {})
    model_var = message_data.get("model_var", {})
    extra = message_data.get("extra", [])

    try:

        # 额外参数 合并到模型参数
        if extra:
            for i in extra:
                model_var[i['key']] = i['value']

        db = MongoDB()
        if message_id != "" and message_index == 0:
            prompt = get_message(message_id=message_id, authorization=authorization, websocket=websocket, db=db,
                                 prompt=prompt)

        try:
            # 添加消息到消息列表
            model_var['messages'] = prompt
            # 发送消息并返回 AI 响应
            chunk_data = await initiate_ai(ai_var=ai_var, model_var=model_var, websocket=websocket)
            # 保存消息
            prompt.append(chunk_data)

            # 如果没有消息id，保存消息
            if message_id == "":
                find_message, error_message = db.insert_one("message",
                                                            {"user_id": authorization, "message": prompt})()
                logger.info(f"消息插入 {error_message}")

                # 生成标题
                model_var['messages'] = prompt


                # 创建聊天记录 并返回id
                chat = await create_new_chat(
                    authorization=authorization,
                    message_id=str(find_message.inserted_id),
                    ai_var=ai_var, model_var=model_var,prompt=message_data.get("prompt", []))
                await ws_send_response(websocket, chat)

            # 如果有消息id，更新消息
            else:
                message, error_message = db.update_one("message",
                                                       {"user_id": authorization, "_id": ObjectId(message_id)},
                                                       {"$addToSet": {"message": {"$each": prompt}}})()
                logger.info(f"消息保存 {message}")
        except Exception as e:
            logger.error(f"请求 AI 时发生错误: {e}")
            await ws_send_response(websocket, f"请求 AI 时发生错误: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        await ws_send_response(websocket, f"数据库错误: {str(e)}", status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"处理 WebSocket 请求时发生错误: {e}")
        await ws_send_response(websocket, f"服务器内部错误: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await websocket.close()
