from pymongo.errors import PyMongoError
from starlette import status
from config import get_logger
from database import MongoDB
from schemas import PromptsResponse

logger = get_logger(__name__)

async def get_prompts(authorization: str) -> PromptsResponse:
    """
    获取预设列表
    :param authorization: 浏览器指纹
    :return: ChatResponse
    """
    try:
        db = MongoDB()
        chat, error_message = db.find("prompts",
                       {"user_id": authorization, "is_del": False},
                       {"is_del": False})()


        if error_message != "":
            logger.error(f"获取用户 {authorization} 的预设时发生错误: {error_message}")
            return PromptsResponse(data=chat, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        logger.info(f"获取用户 {authorization} 的模成功")
        return PromptsResponse(data=chat, status_code=status.HTTP_200_OK, message="成功")

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        return PromptsResponse(data=None, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")

    except Exception as e:
        logger.error(f"获取预设时发生未知错误: {str(e)}")
        return PromptsResponse(data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
