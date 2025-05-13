from pymongo.errors import PyMongoError
from starlette import status
from bson import ObjectId
from config import get_logger
from database import MongoDB
from schemas import ChatResponse

logger = get_logger(__name__)

async def del_model(authorization: str, model_id: str) -> ChatResponse:
    """

    :param authorization: 认证id
    :param model_id: 模型id
    :return:
    """
    try:
        db = MongoDB()
        chat, error_message = db.update_one("model",
                                            {"user_id": authorization, "_id": ObjectId(model_id)},
                                            {"$set": {"is_del": True}})()

        if error_message != "":
            logger.error(f"删除用户 {authorization} 的模型时发生错误: {error_message}")
            return ChatResponse(data=chat, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        logger.info(f"{model_id} 的模型删除成功")
        return ChatResponse(data=chat, status_code=status.HTTP_200_OK, message="成功")

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        return ChatResponse(data={}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")

    except Exception as e:
        logger.error(f"删除模型时发生未知错误: {str(e)}")
        return ChatResponse(data={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
