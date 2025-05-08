from pymongo.errors import PyMongoError
from starlette import status
from bson import ObjectId
from config import get_logger
from database import MongoDB
from schemas import DelChat

logger = get_logger(__name__)

async def del_chat(authorization: str, chat_id: str) -> DelChat:
    try:
        db = MongoDB()
        chat, error_message = db.update_one("chat",
                                            {"user_id": authorization, "_id": ObjectId(chat_id)},
                                            {"$set": {"is_del": True}})()

        if error_message != "":
            logger.error(f"删除用户 {authorization} 的聊天记录时发生错误: {error_message}")
            return DelChat(data=chat, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        logger.info(f"{chat_id} 的聊天删除成功")
        return DelChat(data=chat, status_code=status.HTTP_200_OK, message="成功")

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        return DelChat(data={}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")

    except Exception as e:
        logger.error(f"删除聊天记录时发生未知错误: {str(e)}")
        return DelChat(data={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
