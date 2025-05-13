from audioop import error
from typing import List

from openai import OpenAI
from pymongo.errors import PyMongoError

from config import get_logger
from database import MongoDB

logger = get_logger(__name__)


async def create_new_chat(
        authorization: str,
        message_id: str,
        ai_var: dict,
        model_var: dict, prompt: List[dict], title: str = "unnamed"):
    """
    创建新的聊天记录
    :param authorization: 认证id
    :param message_id: 消息id
    :param ai_var: ai设置
    :param model_var: 模型设置
    :param prompt: 提示（第一句话 ）
    :param title: 标题
    :return:
    """
    if not message_id:
        logger.warning("无消息id，不创建")

    try:

        try:
            # 获取标题
            client = OpenAI(**ai_var).chat.completions.create(
                model=model_var.get("model"),
                stream=False,
                temperature=0.4,
                top_p=1,
                messages=[
                    {'role': 'user', 'content': f"""
Based on the chat history, give this conversation a name.
Keep it short - 10 characters max, no quotes
Use 简体中文.
Just provide the name, nothing else.
Here's the conversation
```
{prompt[0].get('content', "")}
```
Name this conversation in 10 characters or less.
Use 简体中文.
Only give the name, nothing else.
The name is:
"""}
                ]
            )

            title = client.choices[0].message.content


        except error:
            logger.error(f"创建用户 {authorization} 的聊天记录时发生错误: {error}")

        db = MongoDB()
        chat, error_message = db.insert_one("chat",
                       {
                           "user_id": authorization,
                           "message_id": message_id,
                           "title": title,
                           "share": False,
                           "archive": False
                       })()


        if error_message != "":
            logger.error(f"创建用户 {authorization} 的聊天记录时发生错误: {error_message}")
            # return NewChat(data=chat, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        # return NewChat(data=chat, status_code=status.HTTP_200_OK, message="成功"

        return {

            "chat_id": str(chat.inserted_id),
            "message_id": message_id,
            "title": title
        }

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        # return NewChat(data=None, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")
        return {
            "chat_id": None,
            "message_id": None,
            "title": None
        }

    except Exception as e:
        logger.error(f"创建聊天记录时发生未知错误: {str(e)}")
        # return NewChat(data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
        return {
            "chat_id": None,
            "message_id": None,
            "title": None
        }