from pymongo.errors import PyMongoError
from starlette import status
from bson import ObjectId
from config import get_logger
from database import MongoDB
from schemas import PromptsResponse

logger = get_logger(__name__)

async def del_prompts(authorization: str, prompts_id: str) -> PromptsResponse:
    """

    :param authorization: 认证id
    :param prompts_id: 预设id
    :return:
    """
    try:
        db = MongoDB()
        chat, error_message = db.update_one("prompts",
                                            {"user_id": authorization, "_id": ObjectId(prompts_id)},
                                            {"$set": {"is_del": True}})()

        if error_message != "":
            logger.error(f"删除用户 {authorization} 的预设时发生错误: {error_message}")
            return PromptsResponse(data=chat, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        logger.info(f"{prompts_id} 的预设删除成功")
        return PromptsResponse(data=chat, status_code=status.HTTP_200_OK, message="成功")

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        return PromptsResponse(data={}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")

    except Exception as e:
        logger.error(f"删除预设时发生未知错误: {str(e)}")
        return PromptsResponse(data={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
