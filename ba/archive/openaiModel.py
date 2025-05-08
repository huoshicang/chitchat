import json

from fastapi import WebSocket
from openai import OpenAI
from pymongo.errors import PyMongoError
from bson import ObjectId
from starlette import status
from config import get_logger
from database import MongoDB
from schemas import NewMessage
from services.chat.create_new_chat import create_new_chat
from utils import ws_send_response

logger = get_logger(__name__)




async def send_message(websocket: WebSocket, message_data: NewMessage, headers) -> None:
    """
    处理 WebSocket 消息，发送消息并返回 AI 响应。
    """
    authorization = headers.get("authorization", "").replace("Bearer ", "")
    chat_session_id = message_data.get("chat_session_id", "")
    message_id = message_data.get("message_id", 0)
    prompt = message_data.get("prompt", [])
    ai_config = message_data.get("ai_config", {})
    model_config = message_data.get("model_config", {})

    try:
        # 检查消息是否存在，若不存在则插入新消息
        db = MongoDB()

        if message_id == 0 or chat_session_id == "":
            message = prompt

        else:
            message, error_message = db.find_one("message", {"user_id": authorization, "_id": ObjectId(message_id)},
                                  {"message": True, "_id": False})()
            if error_message != "":
                logger.error(f"获取用户 {authorization} 的聊天记录时发生错误: {error_message}")
                await ws_send_response(websocket, f"数据库错误: {error_message}", status.HTTP_400_BAD_REQUEST)
            if message:
                message = message.get("message", [])
                message.extend(prompt)

        try:
            client = OpenAI(api_key=ai_config.get("api_key", ""), base_url=ai_config.get("base_url", ""))

            # 调用 AI 接口
            completion = client.chat.completions.create(**model_config, messages=message)
            receive = ""
            if ai_config.get("stream", True):
                for chunk in completion:
                    data = json.loads(chunk.model_dump_json())
                    if not data:
                        continue
                    receive += data.get('choices', [])[0].get('delta', {}).get("content", "")
                    print(receive)
                    await ws_send_response(websocket, data)
            else:
                print(completion.model_dump_json())
                receive = completion.choices[0].message.content
                await ws_send_response(websocket, json.dumps({}))


            if message_id == "":
                message.extend([{"role": "assistant", "content": receive}])
                message, error_message = db.insert_one("message", {"user_id": authorization, "message": message})()
                logger.info(f"消息插入 {message}")
                # 创建聊天记录 并返回id
                chat = await create_new_chat(authorization=authorization, message_id=str(message.inserted_id))
                await ws_send_response(websocket, chat)
            else:
                message, error_message = db.update_one("message",
                                        {"user_id": authorization, "_id": ObjectId(message_id)},
                                        {
                                            "$push": {
                                                "message": {
                                                    "$each": [
                                                        prompt[0],
                                                        {
                                                            "role": "assistant",
                                                            "content": receive
                                                        }
                                                    ]
                                                }
                                            }
                                        })()
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
