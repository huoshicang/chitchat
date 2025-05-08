from pymongo.errors import PyMongoError
from starlette import status
from bson import ObjectId
from config import get_logger
from database import MongoDB
from schemas import MessageResponse

logger = get_logger(__name__)


async def get_messages(authorization: str, message_id: str) -> MessageResponse:
    try:
        db = MongoDB()
        message, error_message = db.find("message",
                                         {"user_id": authorization, "is_del": 'false', "_id": ObjectId(message_id)},
                                         {"_id": False, })()

        if error_message != "":
            logger.error(f"获取用户 {authorization} 的聊天记录时发生错误: {error_message}")
            return MessageResponse(data=message, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        logger.info(f"获取用户 {authorization} 的记录成功")
        return MessageResponse(data=message, status_code=status.HTTP_200_OK, message="成功")

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        return MessageResponse(data=None, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")

    except Exception as e:
        logger.error(f"获取聊天记录时发生未知错误: {str(e)}")
        return MessageResponse(data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
